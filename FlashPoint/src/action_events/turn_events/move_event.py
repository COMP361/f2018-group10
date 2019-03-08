from abc import ABC

from src.action_events.action_event import ActionEvent
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel


class MoveEvent(ActionEvent):

    def __init__(self, destination: TileModel):
        super().__init__()
        self.tile = destination
        self.player = GameStateModel.instance().players_turn

    def execute(self):
        """Guessing what has to be done is to make everything sync up with the networking"""
        self.player.set_pos(self.tile.x_coord, self.tile.y_coord)
