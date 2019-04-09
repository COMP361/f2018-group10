import logging
from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.drop_hazmat_event import DropHazmatEvent
from src.action_events.turn_events.pick_up_hazmat_event import PickupHazmatEvent
from src.action_events.turn_events.remove_hazmat_event import RemoveHazmatEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import GameKindEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.tile_sprite import TileSprite

logger = logging.getLogger("FlashPoint")


class HazmatController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board
        self._current_player = current_player

        if HazmatController._instance:
            raise Exception("HazmatController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("HazmatController should not exist in Family Mode!")

        HazmatController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def run_checks_drop(self, tile_model: TileModel):
        if isinstance(self._current_player.carrying_hazmat, HazmatModel) and self._current_player.row == tile_model.row \
                and self._current_player.column == tile_model.column:
            return True

        return False

    def run_checks_pickup(self, tile_model: TileModel):
        if isinstance(self._current_player.carrying_victim, VictimModel) or isinstance(self._current_player.carrying_hazmat, HazmatModel):
            return False

        if self._current_player.column == tile_model.column and self._current_player.row == tile_model.row:
            if tile_model.has_hazmat():
                return True
        return False

    def run_checks(self, tile_model: TileModel) -> bool:

        player_tile = self.board.get_tile_at(self._current_player.row, self._current_player.column)

        if not self._current_player == self.game.players_turn:

            return False

        if self._current_player.role != PlayerRoleEnum.HAZMAT:

            return False

        valid_to_do_event = TurnEvent.has_required_AP(self._current_player.ap, 2)
        if not valid_to_do_event:
            return False

        if player_tile.row != tile_model.row or player_tile.column != tile_model.column:
            return False

        if not any([isinstance(model, HazmatModel) for model in tile_model.associated_models]):
            return False

        return True

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        event = None

        if self.run_checks(tile_model):
            event = RemoveHazmatEvent(tile_model.row, tile_model.column)

        elif self.run_checks_pickup(tile_model):

            event = PickupHazmatEvent(tile_model.row, tile_model.column)

        elif self.run_checks_drop(tile_model):

            event = DropHazmatEvent(tile_model.row, tile_model.column)

        if event:
            if Networking.get_instance().is_host:
                Networking.get_instance().send_to_all_client(event)
            else:
                Networking.get_instance().client.send(event)

        menu_to_close.disable()
        menu_to_close.on_click(None)

    def process_input(self, tile_sprite: TileSprite):
        tile = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)
        if self.run_checks(tile):
            tile_sprite.remove_hazmat_button.enable()
            tile_sprite.remove_hazmat_button.on_click\
                (self.send_event_and_close_menu, tile, tile_sprite.remove_hazmat_button)
        else:
            tile_sprite.remove_hazmat_button.disable()

        if self.run_checks_pickup(tile):
            tile_sprite.pickup_hazmat_button.enable()
            tile_sprite.pickup_hazmat_button.on_click\
                (self.send_event_and_close_menu, tile, tile_sprite.pickup_hazmat_button)

        else:
            tile_sprite.pickup_hazmat_button.disable()

        if self.run_checks_drop(tile):
            tile_sprite.drop_hazmat_button.enable()
            tile_sprite.drop_hazmat_button.on_click\
                (self.send_event_and_close_menu, tile, tile_sprite.drop_hazmat_button)
