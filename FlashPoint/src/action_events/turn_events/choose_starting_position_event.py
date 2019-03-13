from src.sprites.game_board import GameBoard
from src.sprites.player_sprite import PlayerSprite
from src.constants.state_enums import GameStateEnum
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
        print("Executing ChooseStartingPositionEvent")
        self.tile.add_associated_model(self.player)
        player_sprite = PlayerSprite(self.player, self.tile, GameBoard.instance().grid)
        GameBoard.instance().add(player_sprite)
        self.player.set_pos(self.tile.row, self.tile.column)
