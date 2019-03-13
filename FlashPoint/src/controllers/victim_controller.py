import pygame

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import WallStatusEnum, GameStateEnum
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.action_events.turn_events.chop_event import ChopEvent
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.game_board import GameBoard
from src.sprites.wall_sprite import WallSprite


class VictimController(object):

    _instance = None
    def __init__(self):

        if VictimController._instance:
            raise Exception("Chop Controller is a singleton")

        VictimController._instance = self

        self.can_drop = False
        self.can_pickup = False


    @classmethod
    def instance(cls):
        return cls.instance()

    def check_pickup(self, tile: TileModel) -> bool:
        game: GameStateModel = GameStateModel.instance()
        victim_tile = game.game_board.get_tile_at(tile.row, tile.column)
        for assoc_model in victim_tile.associated_models:
            if isinstance(assoc_model, VictimModel):
                return True

        return False

    def check_drop(self):
        game: GameStateModel = GameStateModel.instance()
        player = game.players_turn
        if isinstance(player.carrying_victim, VictimModel):
            return True

        return False


    def process_input_(self):
        pass