from src.constants.state_enums import GameKindEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.tile_sprite import TileSprite


class IdentifyController(object):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        if IdentifyController._instance:
            raise Exception("IndentifyController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("IndentifyController should not exist in Family Mode!")

    @classmethod
    def instance(cls):
        return cls._instance

    def process_input(self, tile_sprite: TileSprite):
        pass

    def run_checks(self, tile_model: TileModel):
        pass
