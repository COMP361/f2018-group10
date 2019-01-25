

class FlashPointBaseException(Exception):
    """Base class for FlashPoint specific Exceptions. Please please please use this
    as it will be infinitely valuable for debugging.
    """

    def __init__(self, message: str):
        super().__init__(message)
