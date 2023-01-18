"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import threading, winsound, math
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

import cv2

############
#to implement a coefficient(range from 0 to 1) that combines dist2d_centre and dist3d based on their weights
#the lower the more centered. i.e. 0 means perfectly centered. 
#the further the object, the higher the weight of dist2d_centre (more important to keep it near center)
############

DEBUG = True

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.thread = None
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

    def playsound(self, freq, duration):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=winsound.Beep, args=(freq, duration), daemon=True)
            self.thread.start()

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        dist2d_centre = inputs["dist2d_centre"] #theoretically ranges from 0 to 0.5
        dist3d = inputs["dist3d"] #theoretically ranges from THRESHOLD(i.e. 4) to idk maybe 100+ units
        activate_detection = inputs["activate_detection"]
        with open('sound_mode.txt') as f:
            sound_mode = f.read()

        if sound_mode == 'normal':
            coefficient = -1 #default 

            if activate_detection == True or dist2d_centre == -1 or dist3d == -1: #object not on screen
                if DEBUG:
                    cv2.putText(
                    img=inputs["img"],
                    text = f"centre disabled: {activate_detection}|{dist2d_centre}|{dist3d}",
                    org=(0, 150),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(0,0,255),
                    thickness=3,
                )
            else: #object on screen

                coefficient = round((dist2d_centre)*(1+(math.log(dist3d)-1)/2),3)
                # print(coefficient)

                ### currently for testing purpose ###
                ### To be changed and calibrated to differ from other sound in different situations ###
                
                duration = 80
                f_freq = math.floor(5000 * coefficient)
                # print(f_freq)
                f_freq = min(f_freq, 4500)
                f_freq = max(f_freq, 1100)
                self.playsound(f_freq, duration)

            if DEBUG:
                cv2.putText(
                    img=inputs["img"],
                    text = f"dist2d_centre:{dist2d_centre}",
                    org=(0, 50),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(0,0,255),
                    thickness=3,
                )

                cv2.putText(
                    img=inputs["img"],
                    text = f"coefficient:{coefficient}",
                    org=(0, 100),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(0,0,255),
                    thickness=3,
                )

        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return {}