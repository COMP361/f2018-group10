import pygame
from src.UIComponents.rect_label import RectLabel
from src.action_events.turn_events.choose_starting_position_event import ChooseStartingPositionEvent
from src.constants.state_enums import SpaceKindEnum
from src.core.event_queue import EventQueue
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
import src.constants.color as Color
from src.UIComponents.text import Text
from src.sprites.player_sprite import PlayerSprite


class ChooseStartingPositionController(object):

    def __init__(self, player: PlayerModel, game_board: GameBoard):
        self.player = player
        """The offset of this rectlabel might be wickedly off, please someone has to check it"""
        self.choose_label = RectLabel(500, 0, 300, 75, Color.GREY, 0,
                                      Text(pygame.font.SysFont('Agency FB', 30), "Choose starting position",
                                           Color.ORANGE))
        self.board_state = GameStateModel.instance()
        self.game_board_model = self.board_state.game_board
        self.game_board_sprite = game_board
        self.grid = game_board.grid

    def set_active_labels(self, sprite_grp):
        sprite_grp.add(self.choose_label)

    def update(self, eventq: EventQueue):

        """Loop through the grid to find where the mouse is pointing"""
        for i in range(len(self.grid.grid)):
            for j in range(len(self.grid.grid[i])):
                """1. get the tile at i,j index
                    2. see if that tile is outdoors or indoors
                    3. if indoors: hover is red, cannot click
                    4. if outdoors: hover is green, can click
                    5. if outdoors and clicked, check if there is no player object on that tile
                    6.a if there is a player sprite on that tile: hover red, cant click
                    6b. instantiate ChooseStartingPositionEvent(this curr tile)
                    6-1a. break out of this loop
                    6-1b. delete this controller, """
                curr_tile = self.grid.grid[i][j]
                is_legal = True
                # get associated tile_model
                tile_model = self.game_board_model.get_tile_at(j, i)
                out = tile_model.get_space_kind()

                for models in tile_model.associated_models:
                    if isinstance(models, PlayerModel):
                        is_legal = False

                if is_legal and out == SpaceKindEnum.OUTDOOR:
                    if curr_tile.hover():
                        curr_tile.hover_color = Color.GREEN

                    if curr_tile.is_clicked():

                        event = ChooseStartingPositionEvent(tile_model)
                        self.game_board_sprite.add(PlayerSprite(curr_tile, self.grid))
                        self.choose_label.kill()
                        # delete this controller in case of success scenario, the backend event has been instantiated
                        break

                else:
                    if curr_tile.hover():
                        curr_tile.hover_color = Color.RED
