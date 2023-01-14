"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List, Tuple
import cv2, math
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

def map_bbox_to_image_coords(bbox: List[float], image_size: Tuple[int, int]) -> List[int]:
        """This is a helper function to map bounding box coords (relative) to
        image coords (absolute).
        Bounding box coords ranges from 0 to 1
        where (0, 0) = image top-left, (1, 1) = image bottom-right.

        Args:
            bbox (List[float]): List of 4 floats x1, y1, x2, y2
            image_size (Tuple[int, int]): Width, Height of image

        Returns:
            List[int]: x1, y1, x2, y2 in integer image coords
        """
        width, height = image_size[0], image_size[1]
        x1, y1, x2, y2 = bbox
        x1 *= width
        x2 *= width
        y1 *= height
        y2 *= height
        return int(x1), int(y1), int(x2), int(y2)

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

    def get_speed(self):
        pass

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        img = inputs["img"]
        img_size = (img.shape[1], img.shape[0])  # width, height
        bbox_labels = inputs["bbox_labels"]
        bboxes = inputs["bboxes"]
        obj_person_onscreen = inputs["obj_person_onscreen"]
        loop_count = inputs["loop_count"]

        counter = inputs["counter"]
        counter_refresh = 10
        strict_boundary = 100 #anywhere less than <strict_boundary> pixels away from img boundary is considered object moving out of screen

        prev_coord = inputs["prev_coord"]
        
        obj_person_onscreen_max_length = 20
        obj = 'cell phone'

        #update obj_person_onscreen
        if ("person" in bbox_labels) and (obj in bbox_labels): #both appear 
            if len(obj_person_onscreen) < obj_person_onscreen_max_length:
                obj_person_onscreen.append(True)
            else:
                obj_person_onscreen[loop_count] = True
        else:
            if len(obj_person_onscreen) < obj_person_onscreen_max_length:
                obj_person_onscreen.append(False)
            else:
                obj_person_onscreen[loop_count] = False

        #get speed
        displacement = "Waiting to confirm"
        if obj in bbox_labels:
            # if counter == 0:
            for i, bbox in enumerate(bboxes):
                x1, y1, x2, y2 = map_bbox_to_image_coords(bbox, img_size)
                center_x = math.floor(abs(x2-x1))
                center_y = math.floor(abs(y2-y1))
                current_coord = (center_x,center_y)
                if bbox_labels[i] == obj:
                    x_displacement = abs(current_coord[0]-prev_coord[0])
                    y_displacement = abs(current_coord[1]-prev_coord[1])
                    displacement = math.floor(math.sqrt(x_displacement**2+y_displacement**2))

                    self.logger.info(f"prev:{prev_coord}, curr:{current_coord}")

                    prev_coord = current_coord

        else:
            displacement = "Not defined"
            current_coord = "Not defined"

        safe = 'Not defined'
        if obj in bbox_labels:
            for i, bbox in enumerate(bboxes):
                x1, y1, x2, y2 = map_bbox_to_image_coords(bbox, img_size)
                center_x = math.floor(abs(x2-x1))
                center_y = math.floor(abs(y2-y1))
                if bbox_labels[i] == obj:
                    if strict_boundary<center_x<720-strict_boundary and strict_boundary<center_y<480-strict_boundary:
                        safe = True
                    else: safe = False

        #check if object is blocked by hand
        if obj_person_onscreen.count(True) >= obj_person_onscreen_max_length//2:
            if obj not in bbox_labels:
                obj_blocked_by_hand = True
            else: obj_blocked_by_hand = False
        else: obj_blocked_by_hand = 'Not defined'

        self.logger.info("--------------------------------------------------") #breaklines
        self.logger.info("--------------------------------------------------")
        # self.logger.info(f"bbox_labels:{bbox_labels}")
        self.logger.info(f"obj_person_onscreen:{obj_person_onscreen}")
        self.logger.info(f"loop_count:{loop_count}")
        self.logger.info(f"counter:{counter}")
        

        #cv2
        cv2.putText(
            img=img,
            text = f"displacement:{displacement}",
            org=(0, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0,0,255),
            thickness=3,
         )

        cv2.putText(
            img=img,
            text=f"safe:{safe}",
            org=(0, 100),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0,0,200),
            thickness=3,
         )

        cv2.putText(
            img=img,
            text = f"obj_blocked_by_hand:{obj_blocked_by_hand}",
            org=(0, 150),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0,0,150),
            thickness=3,
         )


        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        outputs = {
            # "obj_blocked_by_hand":obj_blocked_by_hand,
            "obj_person_onscreen": obj_person_onscreen,
            "loop_count":(loop_count+1)%len(obj_person_onscreen),
            "counter":(counter+1)%counter_refresh,
            "prev_coord":prev_coord,
            "obj_blocked_by_hand":obj_blocked_by_hand,
            }
        return outputs