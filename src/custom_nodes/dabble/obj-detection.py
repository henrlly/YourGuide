"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import threading
from pathlib import Path
import numpy as np

import winsound

from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.draw.utils.bbox import draw_bboxes

def filter_bbox(bbox_i, bbox_scores):
    '''return bbox_i with max score'''
    max_score = 0
    max_i = -1
    for i in bbox_i:
        if bbox_scores[i] > max_score:
            max_score = bbox_scores[i]
            max_i = i
    return max_i

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """
    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.thread = None
        self.show_labels = self._get_config_types()["show_labels"]  # type: bool

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
        bbox_scores = inputs["bbox_scores"]
        obj_3D_locs = inputs["obj_3D_locs"]
        bboxes = inputs["bboxes"]

        items_i = []
        persons_i = []
        for i, x in enumerate(bbox_labels):
            if x != "person":
                items_i.append(i)
            else:
                persons_i.append(i)
        
        person_i = filter_bbox(persons_i, bbox_scores)
        item_i = filter_bbox(items_i, bbox_scores)

        if person_i != -1:
            if item_i == -1:
                #only item on screen
                self.playsound(500)

            else:
                #both on screen
                freq = 3000
                #####TODO: change this freq based on distance
                

                
                self.playsound(freq)

        elif item_i != -1:
            #only hand on screen
            self.playsound(300)

        #filter bboxes and labels
        if person_i != -1:
            if item_i != -1:
                n_bboxes = [bboxes[person_i], bboxes[item_i]]
                n_bbox_labels = [bbox_labels[person_i], bbox_labels[item_i]]
            else:
                n_bboxes = [bboxes[person_i]]
                n_bbox_labels = [bbox_labels[person_i]]
        elif item_i != -1:
            n_bboxes = [bboxes[item_i]]
            n_bbox_labels = [bbox_labels[item_i]]
        else:
            n_bboxes = []
            n_bbox_labels = []
        #draw bboxes
        draw_bboxes(
            inputs["img"], n_bboxes, n_bbox_labels, self.show_labels
        )
        return {}

    def _get_config_types(self) -> Dict[str, Any]:
        """Returns dictionary mapping the node's config keys to respective types."""
        return {"show_labels": bool}
