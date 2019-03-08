import pygame
from src.models.game_board.tile_model import TileModel
from src.sprites.tile_sprite import TileSprite
from src.core.networking import Networking
from src.UIComponents.rect_label import RectLabel
from src.action_events.turn_events.choose_starting_position_event import ChooseStartingPositionEvent
from src.constants.state_enums import SpaceKindEnum, GameStateEnum
from src.core.event_queue import EventQueue
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
import src.constants.color as Color
from src.UIComponents.text import Text
from src.sprites.player_sprite import PlayerSprite


class ChooseStartingPositionController(object):

    def __init__(self, game_board_sprite: GameBoard, current_player: PlayerModel):
        self.current_player = current_player
        self.game_board_sprite = game_board_sprite
        self.choose_prompt = RectLabel(500, 0, 350, 75, Color.GREY, 0,
                                       Text(pygame.font.SysFont('Agency FB', 30), "Choose Starting Position",
                                            Color.ORANGE))
        self.wait_prompt = RectLabel(500, 400, 300, 50, Color.GREY, 0,
                                               Text(pygame.font.SysFont('Agency FB', 30), "Wait for your turn!",
                                                    Color.ORANGE))

        self.game_board_sprite.add(self.choose_prompt)
        self.game_board_sprite.add(self.wait_prompt)

    def _apply_hover(self):
        for i in range(len(self.game_board_sprite.grid.grid)):
            for j in range(len(self.game_board_sprite.grid.grid[i])):
                tile_model = GameStateModel.instance().game_board.get_tile_at(j, i)
                tile_sprite = self.game_board_sprite.grid.grid[i][j]

                if not tile_sprite.hover():
                    continue

                if self._run_checks(tile_sprite, tile_model):
                    tile_sprite.hover_color = Color.GREEN
                else:
                    tile_sprite.hover_color = Color.RED

    def _run_checks(self, tile_sprite: TileSprite, tile_model: TileModel) -> bool:
        if GameStateModel.instance().state != GameStateEnum.PLACING:
            return False

        if self.current_player != GameStateModel.instance().players_turn:
            return False

        # Check if any Players are in this tile
        if any([isinstance(model, PlayerModel) for model in tile_model.associated_models]):
            return False

        if tile_model.space_kind == SpaceKindEnum.INDOOR:
            return False

        return True

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self._run_checks(tile_sprite, tile_model):
            return

        event = ChooseStartingPositionEvent(tile_model)
        self.game_board_sprite.add(PlayerSprite(tile_sprite, self.game_board_sprite.grid))
        self.choose_prompt.kill()

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def update(self, event_queue: EventQueue):
        if self.current_player == GameStateModel.instance().players_turn:
            self.wait_prompt.kill()
        if GameStateModel.instance().state == GameStateEnum.PLACING:
            self._apply_hover()
