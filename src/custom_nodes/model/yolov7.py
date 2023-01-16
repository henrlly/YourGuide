
from typing import Any, Dict
import sys, os

sys.path.append('yolov7_files')

import cv2
import numpy as np
import tensorflow as tf

from peekingduck.pipeline.nodes.node import AbstractNode
from peekingduck.pipeline.nodes.draw.utils.bbox import draw_bboxes

import argparse
import time
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

from typing import Any, Dict, List, Optional, Union

IMG_HEIGHT = 640
IMG_WIDTH = 640
SRC = 0

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)

class Node(AbstractNode):
   """Initializes and uses a CNN to predict if an image frame shows a normal
   or defective casting.
   """

   def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
      super().__init__(config, node_path=__name__, **kwargs)
      # self.model = tf.keras.models.load_model('./weights')
      self.source = self.config["source"]
      self.weights, self.imgsz, self.device = f"{self.config['weights'].lower()}.pt", 640, ''
      set_logging()
      self.device = select_device(self.device)
      self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
      self.stride = int(self.model.stride.max())  # model stride
      self.imgsz = check_img_size(self.imgsz, s=self.stride)
      self.iou_thres = self.config['iou_thres']
      self.conf_thres = self.config['conf_thres']
      cudnn.benchmark = True
      if self.device.type != 'cpu':
            self.half = True
            self.model.half()
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once
      else: self.half=False
      self.old_img_w = self.old_img_h = self.imgsz
      self.old_img_b = 1
      self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
      self.names = [x.lower() for x in self.names]
      if self.config['classes'] == ['*']:

            self.classes = [x for x in range(80)]
      else:
            self.classes = [self.names.index(x.lower()) for x in self.config['classes']]
   
   
   def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
      """Reads the image input and returns the predicted class label and
      confidence score.
      
      Args:
            inputs (dict): Dictionary with key "img".

      Returns:
            outputs (dict): Dictionary with keys "pred_label" and "pred_score".
      """
      # img = cv2.cvtColor(inputs["img"], cv2.COLOR_BGR2RGB)
      # img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
      # img = np.expand_dims(img, axis=0)
      # predictions = self.model.predict(img)
      # print(predictions)
      img0 = inputs["img"]
      img = letterbox(img0, self.imgsz, stride=self.stride)[0]
      img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
      img = np.ascontiguousarray(img)
      img = torch.from_numpy(img).to(self.device)
      img = img.half() if self.half else img.float()  # uint8 to fp16/32
      img /= 255.0  # 0 - 255 to 0.0 - 1.0
      if img.ndimension() == 3:
            img = img.unsqueeze(0)

      # Warmup
      # if self.device.type != 'cpu' and (self.old_img_b != img.shape[0] or self.old_img_h != img.shape[2] or self.old_img_w != img.shape[3]):
      #       self.old_img_b = img.shape[0]
      #       self.old_img_h = img.shape[2]
      #       self.old_img_w = img.shape[3]
      #       for i in range(3):
      #             self.model(img, augment=True)[0]

      # Inference
      # t1 = time_synchronized()
      with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
            pred = self.model(img, augment=True)[0]
      # t2 = time_synchronized()

      # Apply NMS
      pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=self.classes, agnostic=True)
      # t3 = time_synchronized()

      bboxes = []
      bbox_labels = []
      bbox_scores = []
      # Process detections
      for i, det in enumerate(pred):  # detections per image
            # gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                  # Rescale boxes from img_size to im0 size
                  det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()


                  # Write results
                  for *xyxy, conf, cls in reversed(det):
                        # print(img.shape)
                        label = f'{self.names[int(cls)]}'
                        score = round(float(conf), 2)
                        bbox = np.array([xyxy[0].item()/img.shape[3], xyxy[1].item()/img.shape[2], xyxy[2].item()/img.shape[3], xyxy[3].item()/img.shape[2]])
                        # print(bbox)
                        bboxes.append(bbox)
                        bbox_labels.append(label)
                        bbox_scores.append(score)
      if self.config['show_bboxes']:
            draw_bboxes(img0, bboxes, bbox_labels, True)
      return {
            "bboxes": bboxes,
            "bbox_labels": bbox_labels,
            "bbox_scores": bbox_scores
      }
   def _get_config_types(self) -> Dict[str, Any]:
        return {
            "classes": List[Union[int, str]],
            "iou_thres": float,
            "conf_thres": float,
            "weights": str,
            'source': Union[int, str],
            'show_bboxes': bool,
        }