"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import cv2
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

DEBUG = False

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """

        bboxes = inputs["n_bboxes"]
        bbox_labels = inputs["n_bbox_labels"]
        
        area = 0 #default
        area_threshold = 0.82 #proportion of screen

        for i, bbox in enumerate(bboxes):
            if bbox_labels[i] != 'person': #object bbox
                x1, y1, x2, y2 = bbox
                area = (x2-x1)*(y2-y1)

        if DEBUG:
            cv2.putText(
                img=inputs["img"],
                text = f"area:{area}",
                org=(0, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0,0,255),
                thickness=3,
            )
            self.logger.info(f'area:{area}')

        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return {"area":area,
        "area_threshold":area_threshold}