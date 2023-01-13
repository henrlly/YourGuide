"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import threading
from pathlib import Path
import pygame

from peekingduck.pipeline.nodes.abstract_node import AbstractNode


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.audio1 = Path(__file__).parent.parent.parent.parent/'sounds'/"beep1.mp3"
        self.thread1 = None
        self.audio2 = Path(__file__).parent.parent.parent.parent/'sounds'/"beep2.mp3"
        self.thread2 = None
        self.audio3 = Path(__file__).parent.parent.parent.parent/'sounds'/"beep3.mp3"
        self.thread3 = None
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")
    def playsound(self, vol, path):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play()
    
    def playsound_thread1(self, vol):
        if self.thread1 is None or not self.thread1.is_alive():
            self.thread1 = threading.Thread(target=self.playsound, args=(vol, self.audio1), daemon=True)
            self.thread1.start()
    def playsound_thread2(self, vol):
        if self.thread2 is None or not self.thread2.is_alive():
            self.thread2 = threading.Thread(target=self.playsound, args=(vol, self.audio2), daemon=True)
            self.thread2.start()
    def playsound_thread3(self, vol):
        if self.thread3 is None or not self.thread3.is_alive():
            self.thread3 = threading.Thread(target=self.playsound, args=(vol, self.audio3), daemon=True)
            self.thread3.start()
    
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        bbox_labels = inputs["bbox_labels"]
        target = [i for i in bbox_labels if i != "person"]
        print(f'bbox_labels: {bbox_labels}')
        if "person" in bbox_labels:
            if len(target) == 0:
                self.playsound_thread1(0.5)
            else:
                #change this volume based on distance
                self.playsound_thread3(0.5)
        elif len(target) > 0:
            self.playsound_thread2(0.5)
        
        
        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return {}
