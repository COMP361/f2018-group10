import logging

from src.sprites.game_board import GameBoard
from src.sprites.player_sprite import PlayerSprite
from src.models.game_units.player_model import PlayerModel
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent


logger = logging.getLogger("FlashPoint")


class ChooseStartingPositionEvent(ActionEvent):
    """This class takes in a tile on instantiation, denoting the starting position"""

    def __init__(self, row: int, column: int):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self._row = row
        self._column = column
        self.player: PlayerModel = game.players_turn

    def execute(self):
        logger.info("Executing ChooseStartingPositionEvent")
        game: GameStateModel = GameStateModel.instance()
        tile = game.game_board.get_tile_at(self._row, self._column)
        player_sprite = PlayerSprite(self.player, tile, GameBoard.instance().grid)
        GameBoard.instance().add(player_sprite)
        self.player.set_pos(tile.row, tile.column)
