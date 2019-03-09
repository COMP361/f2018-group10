from typing import List

import src.constants.color as Color
from src.constants.state_enums import PlayerStatusEnum
from src.observers.player_observer import PlayerObserver
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.action_events.turn_events.extinguish_event import ExtinguishEvent
from src.sprites.tile_sprite import TileSprite
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import SpaceStatusEnum, GameStateEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard


class ExtinguishController(object):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        if ExtinguishController._instance:
            raise Exception("ExtinguishController is a singleton")
        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        game: GameStateModel = GameStateModel.instance()
        game.game_board.reset_tiles_visit_count()
        ExtinguishController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def _run_checks(self, tile_model: TileModel) -> bool:
        player_tile = GameStateModel.instance().game_board.get_tile_at(self.current_player.row, self.current_player.column)
        valid_to_extinguish = tile_model == player_tile or tile_model in player_tile.adjacent_tiles
        if not valid_to_extinguish:
            return False

        if self.current_player.ap < 1:
            return False

        if tile_model.space_status == SpaceStatusEnum.SAFE:
            return False

        return True

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self._run_checks(tile_model):
            return

        event = ExtinguishEvent(self.current_player, tile_model)
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def update(self, event_queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return

        # for column in range(len(self.game_board_sprite.grid.grid)):  # First make them all hover_color to red
        #     for row in range(len(self.game_board_sprite.grid.grid[column])):
        #
        #         tile_model = GameStateModel.instance().game_board.get_tile_at(row, column)
        #         if self._run_checks(tile_model):
        #             self.game_board_sprite.grid.grid[column][row].hover_color = Color.GREEN
        #         else:
        #             self.game_board_sprite.grid.grid[column][row].hover_color = Color.RED
