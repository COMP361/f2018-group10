
from src.models.model import Model


class HazmatModel(Model):

    def __init__(self, row: int, column: int):
        super().__init__()
        self.row = row
        self.column = column