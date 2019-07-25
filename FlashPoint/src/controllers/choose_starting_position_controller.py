import pygame

from src.UIComponents.interactable import Interactable
from src.controllers.controller import Controller
from src.sprites.tile_sprite import TileSprite
from src.core.networking import Networking
from src.UIComponents.rect_label import RectLabel
from src.action_events.turn_events.choose_starting_position_event import ChooseStartingPositionEvent
from src.constants.state_enums import SpaceKindEnum, GameStateEnum
from src.core.event_queue import EventQueue
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
import src.constants.color as Color
from src.UIComponents.text import Text


class ChooseStartingPositionController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if ChooseStartingPositionController._instance:
            self._current_player = current_player
            # raise Exception("ChooseStartingPositionController is a singleton")
        self.current_player = current_player
        self.game_board_sprite = GameBoard.instance()
        self.choose_prompt = RectLabel(500, 30, 350, 75, Color.GREY, 0,
                                       Text(pygame.font.SysFont('Agency FB', 30), "Choose Starting Position",
                                            Color.GREEN2))
        self.choose_prompt.change_bg_image('src/media/GameHud/wood2.png')
        self.choose_prompt.add_frame('src/media/GameHud/frame.png')
        self.wait_prompt = RectLabel(500, 400, 300, 50, Color.GREY, 0,
                                     Text(pygame.font.SysFont('Agency FB', 30), "Wait for your turn!",
                                          Color.GREEN2))
        self.wait_prompt.change_bg_image('src/media/GameHud/wood2.png')
        self.wait_prompt.add_frame('src/media/GameHud/frame.png')

        self.game_board_sprite.top_ui.add(self.choose_prompt)
        self.game_board_sprite.top_ui.add(self.wait_prompt)
        ChooseStartingPositionController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def _apply_hover(self):
        for i in range(len(self.game_board_sprite.grid.grid)):
            for j in range(len(self.game_board_sprite.grid.grid[i])):
                tile_model = GameStateModel.instance().game_board.get_tile_at(j, i)
                tile_sprite = self.game_board_sprite.grid.grid[i][j]

                success = self.run_checks(tile_model)

                if success and not tile_sprite.highlight_color:
                    tile_sprite.highlight_color = Color.GREEN
                elif not success:
                    tile_sprite.highlight_color = None

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        pass

    def run_checks(self, tile_model: TileModel) -> bool:
        if GameStateModel.instance().state != GameStateEnum.PLACING_PLAYERS:
            return False

        if self.current_player != GameStateModel.instance().players_turn:
            return False

        # Check if any Players are in this tile
        if GameStateModel.instance().get_players_on_tile(tile_model.row, tile_model.column):
            return False

        if tile_model.space_kind == SpaceKindEnum.INDOOR:
            return False
        return True

    def process_input(self, tile_sprite: TileSprite):
        if not GameStateModel.instance().players_turn.has_pos:
            tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

            if not self.run_checks(tile_model):
                return

            event = ChooseStartingPositionEvent(tile_model.row, tile_model.column)
            self.choose_prompt.kill()

            if Networking.get_instance().is_host:
                Networking.get_instance().send_to_all_client(event)
            else:
                Networking.get_instance().send_to_server(event)

    def update(self, event_queue: EventQueue):
        if self.current_player == GameStateModel.instance().players_turn:
            self.wait_prompt.kill()
        if GameStateModel.instance().state == GameStateEnum.PLACING_PLAYERS:
            self._apply_hover()
