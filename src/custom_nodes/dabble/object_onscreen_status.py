"""
Node template for creating custom nodes.
"""

###
# obj_person_onscreen, prev_displacements, prev_safe are lists capturing the object status across a short period of time
# these lists are all used to determine whether the object is blocked by hand
###

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

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """
        DEBUG = True #turn this off to remove in-video texts

        img = inputs["img"]
        img_size = (img.shape[1], img.shape[0])  # width, height
        bbox_labels = inputs["n_bbox_labels"]
        bboxes = inputs["n_bboxes"]
        obj_person_onscreen = inputs["obj_person_onscreen"]
        loop_count = inputs["loop_count"]

        counter = inputs["counter"]
        counter_refresh = 20 #frames
        strict_boundary_y = 60 #anywhere less than <strict_boundary> pixels away from img boundary is considered object moving out of screen
        strict_boundary_x = 80

        prev_coord = inputs["prev_coord"]
        prev_displacements = inputs["prev_displacements"]
        prev_displacements_max_length = 10

        displacement_limit = 80 #any displacement above this is considered rigorous movement

        prev_safe = inputs["prev_safe"]
        prev_safe_max_length = 5
        
        obj_person_onscreen_max_length = 10
        with open("specified_object.txt", "r") as f:
            obj = f.read()



        #obj_person_onscreen: both object and person captured
        if ("person" in bbox_labels) and (obj in bbox_labels): #both appear 
            if len(obj_person_onscreen) < obj_person_onscreen_max_length:
                obj_person_onscreen.append(True)
            else:
                obj_person_onscreen[loop_count%obj_person_onscreen_max_length] = True
        else:
            if len(obj_person_onscreen) < obj_person_onscreen_max_length:
                obj_person_onscreen.append(False)
            else:
                obj_person_onscreen[loop_count%obj_person_onscreen_max_length] = False

        #prev_displacement: get displacement per frame
        displacement = "Waiting to confirm"
        if obj in bbox_labels:
            # if counter == 0: #counter refresh
            for i, bbox in enumerate(bboxes):
                x1, y1, x2, y2 = map_bbox_to_image_coords(bbox, img_size)
                center_x = math.floor(abs((x2+x1)/2))
                center_y = math.floor(abs((y2+y1)/2))
                current_coord = (center_x,center_y)
                if bbox_labels[i] == obj:
                    x_displacement = abs(current_coord[0]-prev_coord[0])
                    y_displacement = abs(current_coord[1]-prev_coord[1])
                    displacement = math.floor(math.sqrt(x_displacement**2+y_displacement**2))

                    self.logger.info(f"prev:{prev_coord}, curr:{current_coord}")

                    prev_coord = current_coord #store value
                else: displacement = 0

                if len(prev_displacements) < prev_displacements_max_length:
                    prev_displacements.append(displacement)
                else: prev_displacements[loop_count%prev_displacements_max_length] = displacement


        else:
            displacement = "Not defined"
            current_coord = "Not defined"

        #prev_safe: get safe status
        safe = 'Not defined'
        if obj in bbox_labels:
            for i, bbox in enumerate(bboxes):
                
                if DEBUG:
                    cv2.putText(
                        img=img,
                        text = f"current_coord:{current_coord}",
                        org=(0, 200),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1.0,
                        color=(0,0,255),
                        thickness=3,
                    )
                if bbox_labels[i] == obj:
                    #NOTE: width should be 720 in theory. However, in practice, it seems smaller
                    if strict_boundary_x<center_x<(620-strict_boundary_x) and strict_boundary_y<center_y<(480-strict_boundary_y):
                        safe = True
                    else: 
                        safe = False

        if len(prev_safe) < prev_safe_max_length:
            prev_safe.append(safe)
        else: 
            prev_safe[loop_count%prev_safe_max_length] = safe

        # check if object is blocked by hand
        if (True in obj_person_onscreen):
            if False in prev_safe: #out of scene

                obj_blocked_by_hand = False
                obj_person_onscreen = [False] #renew

            elif any([i for i in prev_displacements if i >= displacement_limit]): 

                obj_blocked_by_hand = False
                obj_person_onscreen = [False] #renew

            elif obj not in bbox_labels and 'person' in bbox_labels: #only hand exists

                obj_blocked_by_hand = True
                obj_person_onscreen = [True] #renew

            else:
                obj_blocked_by_hand = False

        else: obj_blocked_by_hand = 'Not defined'

        # self.logger.info("--------------------------------------------------") #breaklines
        # self.logger.info("--------------------------------------------------")
        # # self.logger.info(f"bbox_labels:{bbox_labels}")
        # self.logger.info(f"obj_person_onscreen:{obj_person_onscreen}")
        # self.logger.info(f"loop_count:{loop_count}")
        # self.logger.info(f"counter:{counter}")
        # self.logger.info(f"prev_displacements:{prev_displacements}")
        # self.logger.info(f"prev_safe:{prev_safe}")
        

        #cv2
        if DEBUG:
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
            "loop_count":(loop_count+1)%100,
            "counter":(counter+1)%counter_refresh,
            "prev_coord":prev_coord,
            "obj_blocked_by_hand":obj_blocked_by_hand,
            "prev_displacements":prev_displacements,
            "prev_safe":prev_safe,
            }
        return outputs