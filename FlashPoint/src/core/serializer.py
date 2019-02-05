import enum
import copy
import inspect
import json
from typing import Dict

from src.core.serializable import Serializable
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
    def _safe_dict(obj):
        obj.__setattr__("class", type(obj).__name__)
        return obj.__dict__ if not isinstance(obj, enum.Enum) else {"name": type(obj).__name__, "value": obj.value}

    @staticmethod
    def serialize(input_obj: object) -> dict:
        """Perform a deep serialize to a dict, then can be dumped into json file."""
        return json.loads(json.dumps(input_obj, default=lambda x: JSONSerializer._safe_dict(x)))
