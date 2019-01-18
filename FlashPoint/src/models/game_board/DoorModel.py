from src.models.game_board.WallModel import WallModel


class DoorModel(WallModel):

    def __init__(self):
        super().__init__()
        self._open = False
