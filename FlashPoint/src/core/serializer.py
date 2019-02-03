import json


class JSONSerializer(object):
    """Used for serializing and deserializing objects to JSON."""

    @staticmethod
    def deserialize(file_path: str) -> object:
        pass

    @staticmethod
    def serialize(input_obj: object) -> dict:
        """Perform a deep serialize to a dict, then can be dumped into json file."""
        return json.loads(json.dumps(input_obj, default=lambda x: x.__dict__))
