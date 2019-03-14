from abc import ABC


class Observer(ABC):
    """
    Interface for Observer objects.
    Extend this for any GUI element that needs to be notified by a GameUnit and/or Model.
    """
