"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import threading
from pathlib import Path
import pygame

import winsound

from peekingduck.pipeline.nodes.abstract_node import AbstractNode


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.thread = None

    def playsound(self, freq):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=winsound.Beep, args=(freq, 100), daemon=True)
            self.thread.start()
    
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        bbox_labels = inputs["bbox_labels"]
        target = [i for i in bbox_labels if i != "person"]
        obj_3D_locs = inputs["obj_3D_locs"]

        print(f'bbox_labels: {bbox_labels}')
        print(f'obj_3D_locs: {obj_3D_locs}')

        if "person" in bbox_labels:
            if len(target) == 0:
                self.playsound(500)
            else:
                freq = 3000
                #####TODO: change this freq based on distance

                self.playsound(freq)
        elif len(target) > 0:
            self.playsound(300)
        
        return {}
