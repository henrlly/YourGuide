"""
Custom node to show object detection scores
"""

from typing import Any, Dict, List, Tuple
import cv2
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

import math
import numpy as np

RED = (0, 0, 255)        # in BGR format, per opencv's convention


def map_bbox_to_image_coords(
   bbox: List[float], image_size: Tuple[int, int]
) -> List[int]:
   """This is a helper function to map bounding box coords (relative) to
   image coords (absolute).
   Bounding box coords ranges from 0 to 1
   where (0, 0) = image top-left, (1, 1) = image bottom-right.

   Args:
      bbox (List[float]): List of 4 floats x1, y1, x2, y2
      image_size (Tuple[int, int]): Width, Height of image

   Returns:
      List[int]: x1, y1, x2, y2 in integer image coords
   """
   width, height = image_size[0], image_size[1]
   x1, y1, x2, y2 = bbox
   x1 *= width
   x2 *= width
   y1 *= height
   y2 *= height
   return int(x1), int(y1), int(x2), int(y2)


class Node(AbstractNode):

   def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
      super().__init__(config, node_path=__name__, **kwargs)

   def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore

      # extract pipeline inputs and compute image size in (width, height)
      img = inputs["img"]
      bboxes = inputs["n_bboxes"]
      obj_3D_locs = inputs["obj_3D_locs"]
      img_size = (img.shape[1], img.shape[0])  # width, height

      for i, bbox in enumerate(bboxes):
         # for each bounding box:
         #   - compute (x1, y1) top-left, (x2, y2) bottom-right coordinates
         #   - convert score into a two decimal place numeric string
         #   - draw score string onto image using opencv's putText()
         #     (see opencv's API docs for more info)
         x1, y1, x2, y2 = map_bbox_to_image_coords(bbox, img_size)
         obj_3D_loc = obj_3D_locs[i]
         obj_3D_loc = np.round(obj_3D_loc,1)
         obj_3D_loc_str = f"{obj_3D_loc}"
         cv2.putText(
            img=img,
            text=obj_3D_loc_str,
            org=(math.floor((x1+x2)/2), math.floor((y1+y2)/2)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,
            color=RED,
            thickness=2,
         )

      return {}               # node has no outputs