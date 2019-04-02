import logging

from src.models.model import Model

logger = logging.getLogger("FlashPoint")

class HazmatModel(Model):

    def __init__(self):
        super().__init__()
        self._row = -7
        self._column = -7

    def __str__(self):
        return f"Hazmat at ({self._row}, {self._column}) "

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def set_pos(self, row: int, column: int):
        self._row = row
        self._column = column
        logger.info(self.__str__())

    def __eq__(self, other):
        if isinstance(other, HazmatModel):
            return True

        return False
