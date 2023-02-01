"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import cv2
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

DEBUG = True

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
        area = inputs["area"]
        prev_area = inputs["prev_area"]
        initial_area = inputs["initial_area"]
        area_shrunk_hist = inputs["area_shrunk_hist"]

        # area_shrunk_lim = 45 #max length: 45 frames (best to follow obj_blocked_by_hand_hist_limit in mission_complete.py)

        #NOTE: setting it to 1 is same as disabling area_shrunk
        area_shrunk_lim = 1 #testing: the previous one is deprecated

        area_shrunk_threshold = initial_area/2
        prev_area_lim = 10 #see the object 10 frames before assinging the average area to intial_area


        object_grabbed_by_hand = "Not defined" #default

        if area != 0:
            if initial_area == 0: #have not initiated
                prev_area.append(area)
                if len(prev_area) == prev_area_lim:
                    initial_area = sum(prev_area)/len(prev_area) #take average for more reliable reading
            else: #have initiated
                if area < area_shrunk_threshold:
                    if len(area_shrunk_hist) < area_shrunk_lim:
                        object_grabbed_by_hand = "Waiting to confirm"
                        area_shrunk_hist.append(True)
                else:
                    object_grabbed_by_hand = False
                    area_shrunk_hist = [] #renew

        if len(area_shrunk_hist) == area_shrunk_lim:
            object_grabbed_by_hand = True
        
        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        if DEBUG:
            cv2.putText(
                img=inputs["img"],
                text = f"object_grabbed_by_hand:{object_grabbed_by_hand}",
                org=(0, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0,0,255),
                thickness=3,
            )
            cv2.putText(
                img=inputs["img"],
                text = f"area:{area}",
                org=(0, 80),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0,0,255),
                thickness=3,
            )
            cv2.putText(
                img=inputs["img"],
                text = f"initial_area:{initial_area}",
                org=(0, 110),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0,0,255),
                thickness=3,
            )
            cv2.putText(
                img=inputs["img"],
                text = f"area_shrunk_hist:{area_shrunk_hist}",
                org=(0, 140),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0,0,255),
                thickness=3,
            )


        return {"object_grabbed_by_hand":object_grabbed_by_hand,
        "area_shrunk_hist":area_shrunk_hist,
        "prev_area":prev_area,
        "initial_area":initial_area}