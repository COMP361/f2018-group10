import logging

from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import GameKindEnum
from src.controllers.controller import Controller
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.tile_sprite import TileSprite

logger = logging.getLogger("FlashPoint")


class CrewChangeController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board
        self._current_player = current_player
        if CrewChangeController.instance():
            raise Exception("CrewChangeController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("CrewChangeController should not exist in Family Mode!")
        CrewChangeController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def process_input(self, tile_sprite: TileSprite):

        assoc_model = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if self.run_checks(assoc_model):
            button = tile_sprite.change_crew_button
            tile_sprite.change_crew_button.on_click(self.send_event_and_close_menu, button)

    def run_checks(self, tile_model: TileModel) -> bool:

        valid_to_do_event = TurnEvent.has_required_AP(self._current_player.ap, 2)

        if not valid_to_do_event:
            return False

        engine_spots = self.board.engine_spots
        player_coord = self._current_player.row,self._current_player.column
        valid_to_do_event = False

        for spots in engine_spots:
            if player_coord[0] == spots[0] and player_coord[1] == spots[1]:
                valid_to_do_event = True

        if not valid_to_do_event:
            return False

        if self._current_player.has_moved:
            return False

        return True

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        pass


