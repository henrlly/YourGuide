from typing import Any, Dict

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

import os

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

        bbox_labels = inputs["bbox_labels"]

        specified_object = None
        with open('specified_object.txt','r') as f:
            specified_object = f.read()

        if specified_object in bbox_labels: #tracker to prevent continuous beeping
            self.logger.info("--------------------------------------------------") #breaklines
            self.logger.info("--------------------------------------------------")
            self.logger.info(f"Specified object <{specified_object}> detected")
            caught = True
        else: 
            caught = False #reset value

        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        outputs = {'caught':caught}
        return outputs