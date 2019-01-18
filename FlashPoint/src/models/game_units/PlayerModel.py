from src.models.game_units.GameUnit import GameUnit


class PlayerModel(GameUnit):

    def __init__(self):
        super().__init__()
        self.user_name = ""
        self.password = ""
        self.status = None   # Should be some status enum

