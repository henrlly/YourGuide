"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
from openal import * 
import threading, time, sys
import numpy as np


from scripts.tts_tool import tts

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

DIST_THRESHOLD = 6

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.thread = None
        self.thread1 = None
        self.thread2 = None

        with open('sound_mode.txt') as f:
            sound_mode = f.read()

        if sound_mode == 'frequency':
            self.is_frequency = True
        else:
            self.is_frequency = False

        with open('specified_object.txt') as f:
            self.obj = f.read()

        self.is_close = False
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

    def playsound_helper(self, duration, x,y,z, filename):
        sleep_time = duration
        source = oalOpen(filename)
        source.set_position([x,y,z])
        source.set_looping(True)
        source.play()
        listener = Listener()
        listener.set_position([0, 0, 0])
        time.sleep(sleep_time)
        oalQuit()
        

    def playsound1(self, duration, x,y,z, filename):
        if self.thread1 is None or not self.thread1.is_alive():
            self.thread1 = threading.Thread(target=self.playsound_helper, args=(duration, x,y,z, filename), daemon=True)
            self.thread1.start()
    def playsound2(self, duration, x,y,z, filename):
        if self.thread2 is None or not self.thread2.is_alive():
            self.thread2 = threading.Thread(target=self.playsound_helper, args=(duration, x,y,z, filename), daemon=True)
            self.thread2.start()

    def tts_wrapper(self, text):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=tts, args=(text,), daemon=True)
            self.thread.start()


    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        bbox_labels = inputs["n_bbox_labels"]
        obj_3D_locs = inputs["obj_3D_locs"]
        dist3d = inputs['dist3d']

        if self.is_frequency:
            if len(bbox_labels)>1 or (bbox_labels!=[] and bbox_labels[0] != "person"):
                a = obj_3D_locs[-1]
                dist3d = np.linalg.norm(a-[0,0,0])
                return {"dist3d":dist3d}
        
        if len(bbox_labels)>1 or (bbox_labels!=[] and bbox_labels[0] != "person"):

            a = obj_3D_locs[-1]
            dist3d = np.linalg.norm(a-[0,0,0])
            # print(dist3d)
            
            if dist3d < DIST_THRESHOLD:
                self.playsound1(0.2, *obj_3D_locs[-1], "sounds/beep-01a.wav")
                # self.tts_wrapper("object close by")
                # self.is_close = True
            else:
                self.playsound1(0.2, *obj_3D_locs[-1], "sounds/beep-07a.wav")

            


        return {"dist3d":dist3d}
