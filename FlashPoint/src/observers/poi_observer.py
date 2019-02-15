from abc import abstractmethod

from src.observers.observer import Observer


class POIObserver(Observer):
    """Base class for getting changes regarding a POI model."""
