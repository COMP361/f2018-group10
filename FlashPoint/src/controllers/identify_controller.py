from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import GameKindEnum
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.sprites.tile_sprite import TileSprite


class IdentifyController(object):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board
        self.current_player = current_player
        if IdentifyController._instance:
            raise Exception("IndentifyController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("IndentifyController should not exist in Family Mode!")

    @classmethod
    def instance(cls):
        return cls._instance

    def check(self, tile_model: TileModel) -> bool:

        if not self.current_player == self.game.players_turn:
            return False

        valid_to_identify = TurnEvent.has_required_AP(self.current_player.ap, 1)
        if not valid_to_identify:
            return False

        for model in tile_model.associated_models:
            if isinstance(model, POIModel):
                return True

        return False

    def process_input(self, tile_sprite: TileSprite):
        tile = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)
        if self.check(tile):
            tile_sprite.identify_button.enable()
        else:
            tile_sprite.identify_button.disable()
