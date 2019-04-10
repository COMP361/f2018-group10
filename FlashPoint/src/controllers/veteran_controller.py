import logging

from src.UIComponents.interactable import Interactable
from src.action_events.veteran_give_experience_event import VeteranGiveExperienceEvent
from src.constants.state_enums import PlayerRoleEnum, PlayerStatusEnum
from src.controllers.controller import Controller
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.player_observer import PlayerObserver
from src.sprites.game_board import GameBoard
from src.sprites.tile_sprite import TileSprite

logger = logging.getLogger("FlashPoint")


class VeteranController(Controller, PlayerObserver):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        if VeteranController._instance:
            raise Exception("VeteranController is a singleton")

        self.game_board_sprite = GameBoard.instance()

        for player in GameStateModel.instance().players:
            player.add_observer(self)

        # self.game.add_observer(self)
        # # Force notify observers
        # self.game.state = self.game.state
        VeteranController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def send_event(self):
        pass
        # event = VeteranGiveExperienceEvent(self._current_player)
        # if Networking.get_instance().is_host:
        #     Networking.get_instance().send_to_all_client(event)
        # else:
        #     Networking.get_instance().send_to_server(event)

    @staticmethod
    def __del__():
        VeteranController._instance = None

    def process_input(self, tile_sprite: TileSprite):
        pass

    def run_checks(self, tile_model: TileModel) -> bool:
        pass

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        pass

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def player_ap_changed(self, updated_ap: int):
        self.send_event()

    def player_special_ap_changed(self, updated_ap: int):
        self.send_event()

    def player_position_changed(self, row: int, column: int):
        self.send_event()

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_carry_changed(self, carry):
        self.send_event()

    def player_role_changed(self, role: PlayerRoleEnum):
        self.send_event()

    def player_leading_victim_changed(self, leading_victim):
        self.send_event()
