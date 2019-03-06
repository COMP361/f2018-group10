from abc import ABC

from src.action_events.action_event import ActionEvent
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel


class Move(ActionEvent):

    def __init__(self, tile_destination: TileModel):
        super().__init__()
        self.destination = tile_destination
        self.is_valid = False
        self.player = GameStateModel.instance().players_turn()

    def check_valid(self):
        num_ap = self.player.ap
        curr_location = GameStateModel.instance().game_board.get_tile_at(self.player.x_pos, self.player.y_pos)
        cost = 0
        cost = self.compute_distance(curr_location, cost)

    def compute_distance(self, curr_location: TileModel, cost: int):
        pass

    def execute(self):
        pass
