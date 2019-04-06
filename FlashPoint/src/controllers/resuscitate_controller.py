from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import GameKindEnum, WallStatusEnum, DoorStatusEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.door_model import DoorModel
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.tile_sprite import TileSprite


class ResuscitateController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board
        self._current_player = current_player

        if ResuscitateController._instance:
            raise Exception("ResuscitateController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("ResuscitateController should not exist in Family Mode!")

        ResuscitateController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def run_checks(self, tile_model: TileModel) -> bool:
       
        player_tile = self.board.get_tile_at(self._current_player.row, self._current_player.column)

        if not self._current_player == self.game.players_turn:
            return False

        if self._current_player.role != PlayerRoleEnum.PARAMEDIC:
            return False

        valid_to_do_event = TurnEvent.has_required_AP(self._current_player.ap, 1)
        if not valid_to_do_event:
            return False

        if player_tile.row != tile_model.row or player_tile.column != tile_model.column:
            return False

        if not any([isinstance(model, VictimModel) for model in tile_model.associated_models]):
            return False

        return True

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.run_checks(tile_model):
            menu_to_close.disable()
            return

       ## event = Resucistate(tile_model.row, tile_model.column)
       ## event = HazmatEvent(tile_model.row, tile_model.column)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)
        menu_to_close.disable()
        menu_to_close.on_click(None)

    def process_input(self, tile_sprite: TileSprite):
        tile = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)
        if self.run_checks(tile):
            tile_sprite.resuscitate_button.enable()
            tile_sprite.on_click(self.send_event_and_close_menu, tile, tile_sprite.resuscitate_button)
        else:
            tile_sprite.resuscitate_button.disable()

