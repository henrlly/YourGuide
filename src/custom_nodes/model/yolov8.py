"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List, Optional, Union
import numpy as np

import torch

from ultralytics import YOLO
from ultralytics.yolo.utils.ops import non_max_suppression

from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.draw.utils.bbox import draw_bboxes


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.model = YOLO(self.config['weights']+'.pt')
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")
        self.names  =['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
        
        if self.config['conf_thres']== -1:
            self.config['conf_thres'] = 0.25
        if self.config['iou_thres'] == -1:
            self.config['iou_thres'] = 0.45
        if self.config['classes'] != ['*']:
            self.cls = [self.names.index(x) for x in self.config['classes']]
        else:
            self.cls = [i for i in range(80)]
        print(self.model.overrides['cfg'])
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        img = inputs["img"]
        result = self.model.predict(source=img, imgsz=640, conf=self.config['conf_thres'], iou=self.config['iou_thres'])[0]

        
        bboxes = []
        bbox_labels = []
        bbox_scores = []

        for i,x in enumerate(result.boxes.cls.cpu().numpy()):
            if x in self.cls:
                bboxes.append(result.boxes.xyxyn.cpu().numpy()[i])
                bbox_labels.append(self.names[int(result.boxes.cls.cpu().numpy()[i])])
                bbox_scores.append(result.boxes.conf.cpu().numpy()[i])

        
        if self.config['show_bboxes']:
                draw_bboxes(img, bboxes, bbox_labels, True)
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
            'show_bboxes': bool,
        }