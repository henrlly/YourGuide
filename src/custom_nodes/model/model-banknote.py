"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
from ultralytics import YOLO
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import threading, cv2
from peekingduck.pipeline.nodes.abstract_node import AbstractNode


from scripts.tts_tool import tts


IMG_SIZE = (224, 224)
DEBUG = False



class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        
        self.labels = ['100_1', '100_2', '10_1', '10_2', '2_1', '2_2', '50_1', '50_2', '5_1', '5_2', 'unknown']
        self.audiocues = ['100 face up', '100 face down', '10 face up', '10 face down', '2 face up', '2 face down', '50 face up', '50 face down', '5 face up', '5 face down', 'unknown']
        self.thread = None
        self.model = YOLO(self.config['model'] + '.pt')

        #trailing list of previous predictions, used to filter out background images
        self.prev_preds = {x:0 for x in self.labels}
        self.prev_preds_lst = []
        self.curr_prev_preds_length = 0

        self.prev_preds_length = self.config['prev_preds_length']
        self.prev_preds_thres = int(self.config['prev_preds_length'] * self.config['prev_preds_thres'])
        self.filter_threshold = self.config['filter_threshold']

        self.label = 'unknown'

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
        img = inputs["img"]
        
        predictions = self.model(img)[0]
        predictions = predictions.probs.cpu().numpy()
        f_predictions = np.argmax(predictions, axis=0)
        prob = predictions[f_predictions]
        if prob < self.filter_threshold:
            cur_label = 'unknown'
        else:
            cur_label = self.labels[f_predictions]

        self.prev_preds[cur_label] += 1
        self.prev_preds_lst.append(cur_label)
        if self.prev_preds[cur_label] > self.prev_preds_thres:
            if self.label != cur_label:
                self.label = cur_label
                ### audio sound ###
                if self.label != 'unknown':
                    cue = self.audiocues[self.labels.index(self.label)]
                    self.tts_wrapper(cue)

            
        if len(self.prev_preds) > self.prev_preds_length:
            pred = self.prev_preds_lst.pop(0)
            self.prev_preds[pred] -= 1
        if DEBUG:
            cv2.putText(
            img=inputs["img"],
            text = f"label: {self.label}",
            org=(0, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0,0,255),
            thickness=3,
            )
            cv2.putText(
            img=inputs["img"],
            text = f"cur_label: {cur_label}",
            org=(0, 100),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0,0,255),
            thickness=3,
            )
            cv2.putText(
            img=inputs["img"],
            text = f"prob: {prob}",
            org=(0, 150),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0,0,255),
            thickness=3,
                )    
        return {}
    def _get_config_types(self) -> Dict[str, Any]:
        return {
            "filter_threshold": float,
            'prev_preds_length': int,
            'prev_preds_thres': float
        }
