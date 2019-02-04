import enum
import copy
import inspect
import json
from typing import Dict

from src.models.game_units.player_model import PlayerModel


class JSONSerializer(object):
    """Used for serializing and deserializing objects to JSON."""

    @staticmethod
    def deserialize(payload: Dict) -> object:
        """
        Grab an object and deserialize it.
        Note that the object must be able to take a dict as input. If there are nested objects or enums in the object,
        it must define its own _deserialize method by implementing the Serializable abstract class.

        Add to this case statement to be able to deserialize your object type.
        """
        object_type = payload["class"]
        if object_type == PlayerModel.__name__:
            return PlayerModel(payload)

        print("WARNING: Could not deserialize object, not of recognized type.")

    @staticmethod
    def serialize(input_obj: object) -> dict:
        """Perform a deep serialize to a dict, then can be dumped into json file."""
        attributes = inspect.getmembers(input_obj)
        copied = copy.deepcopy(input_obj)
        payload = input_obj

        for attr in attributes:
            if isinstance(attr[1], enum.Enum):
                copied.__setattr__(attr[0], {"name": type(attr[1]).__name__, "value": attr[1].value})
                payload = copied

        payload.__setattr__("class", type(payload).__name__)
        return json.loads(json.dumps(payload, default=lambda x: x.__dict__))
