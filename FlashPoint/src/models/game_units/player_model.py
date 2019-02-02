import src.constants.color as Color
from models.game_board.tile_model import TileModel
from src.constants.state_enums import PlayerStatusEnum
from src.models.game_units.game_unit import GameUnit


class PlayerModel(GameUnit):

    def __init__(self, tile: TileModel):
        super().__init__(tile)
        self._user_name = ""
        self._password = ""
        self._color = Color.WHITE  # White by default (not racist I swear)
        self._status = PlayerStatusEnum.OFFLINE
        self._ability_points = 0

    def _validate_tile(self, tile: TileModel):
        # TODO: Implement this
        pass
