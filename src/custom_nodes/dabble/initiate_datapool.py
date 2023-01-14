"""
Node template for creating custom nodes.
"""

from typing import Any, Dict

from peekingduck.pipeline.nodes.abstract_node import AbstractNode


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
        data_pool = list(inputs.keys())
        if "obj_person_onscreen" not in data_pool and "loop_count" not in data_pool:
            obj_person_onscreen = []
            loop_count = 0
        else:
            obj_person_onscreen = inputs["obj_person_onscreen"]
            loop_count = inputs["loop_count"]

        if "counter" not in data_pool: #a counter used to achieve time.sleep effect
            counter = 0
        else:
            counter = inputs["counter"]

        if "prev_coord" not in data_pool:
            prev_coord = (0,0)
        else:
            prev_coord = inputs["prev_coord"]


        outputs = {"obj_person_onscreen":obj_person_onscreen,
        "loop_count":loop_count,
        "counter":counter,
        "prev_coord":prev_coord}
        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return outputs