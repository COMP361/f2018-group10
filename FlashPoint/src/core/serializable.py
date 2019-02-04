import json
from abc import ABC, abstractmethod
from typing import Dict


class Serializable(ABC):
    """Interface for implementing serializable classes"""

    @abstractmethod
    def _deserialize(self, json_payload: Dict):
        self.__dict__ = json.loads(str(json_payload))
