from typing import Any

from prompt_collapse.state import State
from .registry import TRANSFORMATION_REGISTRY

from .transformation import Transformation


class ReplaceNoneTransformation(Transformation):
    def __init__(self, transformation: Transformation) -> None:
        self._transformation = transformation

    @classmethod
    def from_spec(cls, spec: Any) -> "ReplaceNoneTransformation":
        if not isinstance(spec, dict):
            raise ValueError(f"Expected a dictionary, but got {spec}")

        transformation = TRANSFORMATION_REGISTRY.parse(spec.get("transform"))

        return cls(transformation)

    def apply(self, value: Any, local_state: State, global_state: State) -> Any:
        """
        Replacing the current value with the value of the specified variable in one of the provided states.
        The lookup order is local state -> global state, similar to the variable lookup order in Python.

        :param value: The value to replace
        :param local_state: The local state
        :param global_state: The global state
        :return: The value of the specified variable
        """

        if value is None:
            return self._transformation.apply(value, local_state, global_state)

        return value
