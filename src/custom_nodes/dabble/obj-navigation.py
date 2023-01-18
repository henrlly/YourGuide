"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
from openal import * 
import threading, time
import numpy as np

from scripts.tts_tool import tts

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

DIST_THRESHOLD = 4

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.thread = None
        self.thread1 = None
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

    def playsound_helper(self, duration, x,y,z):
        sleep_time = duration
        source = oalOpen("sounds/beep-01a.wav")
        source.set_position([x,y,z])
        source.set_looping(True)
        source.play()
        listener = Listener()
        listener.set_position([0, 0, 0])

        y_pos = 5
        time.sleep(sleep_time)
        oalQuit()

    def playsound1(self, duration, x,y,z):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.playsound_helper, args=(duration, x,y,z), daemon=True)
            self.thread.start()

    def tts_wrapper(self, text):
        if self.thread1 is None or not self.thread1.is_alive():
            self.thread1 = threading.Thread(target=tts, args=(text,), daemon=True)
            self.thread1.start()


    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        bbox_labels = inputs["n_bbox_labels"]
        obj_3D_locs = inputs["obj_3D_locs"]
        if inputs["activate_detection"]:
            return {"activate_detection": True}

        if len(bbox_labels)>1 or (bbox_labels!=[] and bbox_labels[0] != "person"):
            self.playsound1(0.2, *obj_3D_locs[-1])

            #3d dist
            a = obj_3D_locs[-1]
            dist3d = np.linalg.norm(a-[0,0,0])
            if dist3d < DIST_THRESHOLD:
                self.tts_wrapper("Activating detection")
                return {"activate_detection": True}
            print('3d dist: ', dist3d)

        return {"activate_detection": False}
