import pygame

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import WallStatusEnum, GameStateEnum
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.action_events.turn_events.chop_event import ChopEvent
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.sprites.wall_sprite import WallSprite


class ChopController(object):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        if ChopController._instance:
            raise Exception("Chop Controller is a singleton")
        self.current_player = current_player
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board
        ChopController._instance = self
        self.to_chop: WallSprite = None
        self.chop_able = False

    @classmethod
    def instance(cls):
        return cls._instance

    def check(self, wall: WallModel) -> bool:
        if not self.current_player == self.game.players_turn:
            return False

        valid_to_chop = TurnEvent.has_required_AP(self.current_player.ap, 2)
        if not valid_to_chop:
            return False

        player_tile = self.board.get_tile_at(self.current_player.row, self.current_player.column)

        if wall not in player_tile.adjacent_edge_objects.values():
            return False

        wall_status = wall.wall_status
        if wall_status == WallStatusEnum.DESTROYED:
            return False

        return True

    def process_input(self, wall_sprite: WallSprite):
        wall_model = wall_sprite.wall

        if self.to_chop:
            self.to_chop.disable_chop()
            self.to_chop.button_input.disable()
            self.to_chop = None

        if not self.check(wall_model):
            wall_sprite.disable_chop()
            self.chop_able = False
            return

        self.chop_able = True
        wall_sprite.enable_chop()
        self.to_chop = wall_sprite
        self.to_chop.button_input.enable()
        self.to_chop.button_input.on_click(self.instantiate_event, self.to_chop)

    def instantiate_event(self, wall_sprite: WallSprite):

        wall = wall_sprite.wall
        if not self.check(wall):
            return

        event = ChopEvent(wall)
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

    def update(self, event_queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return

        walls = GameBoard.instance().grid.get_walls

        for wall in walls:
            for event in event_queue:
                if event.type == pygame.MOUSEBUTTONUP:
                    if wall.direction == 'North' or wall.direction == 'South':  # means the wall is horizontal
                        if wall.button.rect.x <= pygame.mouse.get_pos()[
                            0] <= wall.button.rect.x + 100 and wall.button.rect.y <= \
                                pygame.mouse.get_pos()[1] <= wall.button.rect.y + 25:
                            # means the user is pressing on the wall
                            print("wall detected")
                            self.process_input(wall)

                    else:  # means the wall is vertical
                        if wall.button.rect.x <= pygame.mouse.get_pos()[
                            0] <= wall.button.rect.x + 25 and wall.button.rect.y <= \
                                pygame.mouse.get_pos()[1] <= wall.button.rect.y + 100:
                            # means the user is pressing on the wall
                            print("wall detected")
                            self.process_input(wall)
