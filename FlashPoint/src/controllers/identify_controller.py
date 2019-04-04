from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.identify_poi_event import IdentifyPOIEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import GameKindEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.sprites.tile_sprite import TileSprite


class IdentifyController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board
        if IdentifyController._instance:
            raise Exception("IndentifyController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("IndentifyController should not exist in Family Mode!")

        IdentifyController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def run_checks(self, tile_model: TileModel) -> bool:
        if not self._current_player == self.game.players_turn:
            return False

        if self._current_player.role != PlayerRoleEnum.IMAGING:
            return False

        if not TurnEvent.has_required_AP(self._current_player.ap, 1):
            return False

        for model in tile_model.associated_models:
            if isinstance(model, POIModel):
                return True

        return False

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.run_checks(tile_model):
            return
        event = IdentifyPOIEvent(tile_model.row, tile_model.column)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def process_input(self, tile_sprite: TileSprite):
        tile_model = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)
        if self.run_checks(tile_model):
            tile_sprite.identify_button.enable()
        else:
            tile_sprite.identify_button.disable()

        tile_sprite.identify_button.on_click(self.send_event_and_close_menu, tile_model, tile_sprite.identify_button)
