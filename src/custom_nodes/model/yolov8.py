"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import numpy as np

from ultralytics import YOLO




from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.draw.utils.bbox import draw_bboxes


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.model = YOLO('yolov8n.pt')
        self.model.fuse()  
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")
        self.names  =['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        img = inputs["img"]
        outputs = self.model.predict(source=img, stream=True)
        bboxes = []
        bbox_labels = []
        bbox_scores =  []
        # for output in outputs:
        #     print(output)
            # if output.boxes.xyxyn != []:
            #     bboxes.append(output.boxes.xyxyn)
            #     bbox_labels.append(self.names[int(output.boxes.cls)])
            #     bbox_scores.append(float(output.boxes.conf))
        # for tracking

        # draw_bboxes(inputs["img"], bboxes, bbox_labels, True)
        return {
            # "bboxes": bboxes,
            # "bbox_labels": bbox_labels,
            # "bbox_scores": bbox_scores
        }
    # def _get_config_types(self) -> Dict[str, Any]:
    #     return {
    #         "classes": List[Union[int, str]],
    #         "iou_thres": float,
    #         "conf_thres": float,
    #         "weights": str,
    #         'source': Union[int, str],
    #         'show_bboxes': bool,
    #     }