from src.models.model import Model


class HazmatModel(Model):

    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, HazmatModel):
            return False
        return True
