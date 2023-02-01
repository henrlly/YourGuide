"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import cv2
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

from scripts.tts_tool import tts

DEBUG = False

AUTO_EXIT = True #turn this off to disable this feature

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

        with open('specified_object.txt') as f:
            self.specified_object = f.read()

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """

        obj_blocked_by_hand_hist = inputs["obj_blocked_by_hand_hist"]
        obj_blocked_by_hand = inputs["obj_blocked_by_hand"]
        object_grabbed_by_hand = inputs["object_grabbed_by_hand"]

        area = inputs["area"]
        area_threshold = inputs["area_threshold"]

        obj_blocked_by_hand_hist_limit = 45 #blocked for 45 frames

        if obj_blocked_by_hand == True: #must be True and not any other value
            obj_blocked_by_hand_hist.append(True)
        else:
            obj_blocked_by_hand_hist = [] #renew

        if len(obj_blocked_by_hand_hist) > obj_blocked_by_hand_hist_limit: #condition 1: small objects blocked by hand
            mission_complete = True
            self.logger.info('Mission complete: object blocked by hand')
        elif object_grabbed_by_hand == True:
            mission_complete = True
            self.logger.info('Mission complete: object grabbed by hand')
        elif area > area_threshold: #condition 2: door/ could be any large object
            mission_complete = True
            self.logger.info('Mission complete: large object very close to user')
        else:
            mission_complete = False

        if DEBUG:
            self.logger.info("obj_blocked_by_hand_hist:{obj_blocked_by_hand_hist}")

            cv2.putText(
                img=inputs["img"],
                text=f"mission_complete:{mission_complete}",
                org=(240,320),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                color=(255,255,0),
                thickness=2,
            )
        
        if AUTO_EXIT and mission_complete:
            if self.specified_object == 'door': #may change in the future to include large objects
                tts(f'The {self.specified_object} is right in front of you, exiting program in three. two. one.') 
            else:
                tts(f'{self.specified_object} reached, exiting program in three. two. one.')

            self.logger.info(f'\n{self.specified_object} reached, exiting program...\n')

            exit() 


        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return {"obj_blocked_by_hand_hist":obj_blocked_by_hand_hist}