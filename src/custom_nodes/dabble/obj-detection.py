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


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """
    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.thread = None

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
        bbox_labels = inputs["bbox_labels"]
        bbox_scores = inputs["bbox_scores"]
        obj_3D_locs = inputs["obj_3D_locs"]
        bboxes = inputs["bboxes"]

        max_score_p = 0
        max_score_item = 0
        person_i = -1
        item_i = -1

        for i, x in enumerate(bbox_labels):
            if x == "person":
                if bbox_scores[i] > max_score_p:
                    max_score_p = bbox_scores[i]
                    person_i = i
            else:
                if bbox_scores[i] > max_score_item:
                    max_score_item = bbox_scores[i]
                    item_i = i
        

        if person_i != -1:
            if item_i == -1:
                #only item on screen
                self.playsound(500, 100)

            else:
                #both on screen
                freq = 500
                duration = 80
                #####TODO: change this freq based on distance

                #3d distance
                a = obj_3D_locs[person_i]
                b = obj_3D_locs[item_i]
                dist3d = np.linalg.norm(a-b)
                print(dist3d)

                #2d distance
                # px = (bboxes[person_i][0], bboxes[person_i][2])
                # py = (bboxes[person_i][1], bboxes[person_i][3])
                # ix = (bboxes[item_i][0], bboxes[item_i][2])
                # iy = (bboxes[item_i][1], bboxes[item_i][3])
                a = np.array(((bboxes[person_i][2] + bboxes[person_i][0])/2, (bboxes[person_i][3] + bboxes[person_i][1])/2))
                b = np.array(((bboxes[item_i][2] + bboxes[item_i][0])/2, (bboxes[item_i][3] + bboxes[item_i][1])/2))
                print(a, b)
                dist2d = np.linalg.norm(a-b)
                print(f'dist2d:{dist2d}')
                
                #min 2d distance
                # if px[0] >= ix[0] and px[0] <= ix[1]:
                #     #within x range
                #     if py[0] >= iy[0] and py[0] <= iy[1]:
                #         #within y range
                #         dist2d = 0
                #     else:
                #         dist2d = min(abs(py[0] - iy[0]), abs(py[0] - iy[1]))
                # else:
                #     if py[0] >= iy[0] and py[0] <= iy[1]:
                #         #within y range
                #         dist2d = min(abs(px[0] - ix[0]), abs(px[0] - ix[1]))
                #     else:
                #         dist2d = min(np.linalg.norm(np.array((px[0], py[0])) - np.array((ix[0], iy[0]))), np.linalg.norm(np.array((px[0], py[0])) - np.array((ix[1], iy[1]))))

                # print(dist2d)


                self.playsound(int(5000 - 4000*dist2d), duration)

        elif item_i != -1:
            #only hand on screen
            self.playsound(300, 100)

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
            inputs["img"], n_bboxes, n_bbox_labels, True
        )
        return {"n_bboxes": n_bboxes, "n_bbox_labels":n_bbox_labels}
