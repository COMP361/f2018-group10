from src.models.game_units.player_model import PlayerModel
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.models.game_board.tile_model import TileModel


class ChooseStartingPositionEvent(ActionEvent):
    """This class takes in a tile on instantiation, denoting the starting position"""

    def __init__(self, tile_position: TileModel):
        super().__init__()
        self.tile = tile_position
        self.player: PlayerModel = GameStateModel.instance().players_turn

    def execute(self):
        """TODO: Fill execute method. Have to get to current game state and find reference to curr_player """
        """Other complication might be to get to reference of the current player. I added Enum for the game state"""
        self.tile.add_associated_model(self.player)
        self.player.set_pos(self.tile.x_coord, self.tile.y_coord)

