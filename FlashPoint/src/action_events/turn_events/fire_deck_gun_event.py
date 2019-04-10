import logging
import random

from src.UIComponents.file_importer import FileImporter
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import VehicleOrientationEnum, QuadrantEnum, SpaceStatusEnum, DoorStatusEnum, \
    WallStatusEnum, PlayerRoleEnum
from src.core.flashpoint_exceptions import FlippingDiceProblemException
from src.models.game_board.door_model import DoorModel
from src.models.game_board.null_model import NullModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard

logger = logging.getLogger("FlashPoint")


class FireDeckGunEvent(TurnEvent):

    def __init__(self, seed: int = 0, row: int = -1, column: int = -1):
        super().__init__()
        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed
        self.row = row
        self.col = column
        # Pick random location: roll dice
        random.seed(self.seed)
        game: GameStateModel = GameStateModel.instance()
        self.player = game.players_turn
        self.engine = game.game_board.engine
        if row > -1 and column > -1:
            self.target_tile: TileModel = game.game_board.get_tile_at(self.row, self.col)
        else:
            self.target_tile = NullModel()

    def execute(self, *args, **kwargs):
        logger.info("Executing Fire Deck Gun Event")

        self.game: GameStateModel = GameStateModel.instance()

        if isinstance(self.target_tile, NullModel):
            self._set_target_tile()
        
        self.target_tile.space_status = SpaceStatusEnum.SAFE

        FileImporter.play_music("media/music/water_splash.mp3", 1)
        tile_sprite = GameBoard.instance().grid.grid[self.target_tile.column][self.target_tile.row]
        tile_sprite.fire_deck_gun = True

        directions = ["North", "East", "West", "South"]
        for dirn in directions:
            has_obstacle = self.target_tile.has_obstacle_in_direction(dirn)
            obstacle = self.target_tile.get_obstacle_in_direction(dirn)
            # If there is no obstacle in the given direction or there is an
            # open door, set the status of the space in that direction to Safe.
            if not has_obstacle or (isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.OPEN)\
                    or (isinstance(obstacle, WallModel) and obstacle.wall_status == WallStatusEnum.DESTROYED):
                nb_tile: TileModel = self.target_tile.get_tile_in_direction(dirn)
                nb_tile.space_status = SpaceStatusEnum.SAFE
                tile_sprite = GameBoard.instance().grid.grid[nb_tile.column][nb_tile.row]
                tile_sprite.fire_deck_gun = True

        if self.player.role == PlayerRoleEnum.DRIVER:
            self.player.ap = self.player.ap - 2
        else:
            self.player.ap = self.player.ap - 4

    def _set_target_tile(self):
        """
        Set the tile which will be the
        target for the firing of the deck gun.

        :return:
        """
        engine_quadrant = self._determine_quadrant(self.engine.row, self.engine.column)
        target_row = GameStateModel.instance().roll_red_dice()
        target_column = GameStateModel.instance().roll_black_dice()
        target_quadrant = self._determine_quadrant(target_row, target_column)
        # If the roll gives a tile in the engine's
        # quadrant, that will become the target tile.
        if target_quadrant == engine_quadrant:
            self.target_tile = GameStateModel.instance().game_board.get_tile_at(target_row, target_column)
            return

        else:
            # Flipping the red dice involves
            # subtracting the roll value from 7.
            flipped_row = 7 - target_row
            # Try out the following combinations
            # and see if any of them are in the
            # engine's quadrant:
            # 1. flipping the row, same column
            # 2. same row, flipping the column
            # 3. flipping the row, flipping the column
            new_target_quadrant = self._determine_quadrant(flipped_row, target_column)
            if new_target_quadrant == engine_quadrant:
                self.target_tile = GameStateModel.instance().game_board.get_tile_at(flipped_row, target_column)
                return

            flipped_column = GameStateModel.instance().determine_black_dice_opposite_face(target_column)
            new_target_quadrant = self._determine_quadrant(target_row, flipped_column)
            if new_target_quadrant == engine_quadrant:
                self.target_tile = GameStateModel.instance().game_board.get_tile_at(target_row, flipped_column)
                return

            new_target_quadrant = self._determine_quadrant(flipped_row, flipped_column)

            if new_target_quadrant == engine_quadrant:
                self.target_tile = GameStateModel.instance().game_board.get_tile_at(flipped_row, flipped_column)
                return

        # $$$$$$$$$$$$$$$$$
        # Shouldn't be able to reach this point!!
        # One of the cases above should have worked.
        # $$$$$$$$$$$$$$$$$
        logger.error("Possible issue with dice flipping! Stop!!")
        raise FlippingDiceProblemException()

    def _determine_quadrant_player(self, row, column) -> QuadrantEnum:
        """
        Determines the quadrant to which
        the row and column belong to.

        :param row:
        :param column:
        :return: Quadrant in which the row and
                column are located.
        """
        if 4 > row > 0 and 5 > column > 0:
            return QuadrantEnum.TOP_LEFT
        elif 4 > row > 0 and 5 <= column < 9:
            return QuadrantEnum.TOP_RIGHT
        elif 4 <= row < 7 and 5 > column > 0:
            return QuadrantEnum.BOTTOM_LEFT
        elif 4 <= row < 7 and 5 <= column < 9:
            return QuadrantEnum.BOTTOM_RIGHT

    def _determine_quadrant(self, row, column) -> QuadrantEnum:
        """
        Determines the quadrant to which
        the row and column belong to.

        :param row:
        :param column:
        :return: Quadrant in which the row and
                column are located.
        """
        if row < 4 and column < 5:
            return QuadrantEnum.TOP_LEFT
        elif row < 4 and column >= 5:
            return QuadrantEnum.TOP_RIGHT
        elif row >= 4 and column < 5:
            return QuadrantEnum.BOTTOM_LEFT
        else:
            return QuadrantEnum.BOTTOM_RIGHT

    def _are_players_in_quadrant(self, quadrant: QuadrantEnum) -> bool:
        """
        Determines whether there are any players
        in the given quadrant.

        :param quadrant: Quadrant that we are interested in.
        :return: True if there are players in the quadrant,
                False otherwise.
        """

        for player in GameStateModel.instance().players:

            if quadrant == self._determine_quadrant_player(self.player.row, self.player.column):
                return True

        return False
