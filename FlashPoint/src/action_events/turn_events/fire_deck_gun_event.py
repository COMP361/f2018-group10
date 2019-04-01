import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import VehicleOrientationEnum, QuadrantEnum, SpaceStatusEnum, DoorStatusEnum
from src.core.flashpoint_exceptions import FlippingDiceProblemException
from src.models.game_board.door_model import DoorModel
from src.models.game_board.null_model import NullModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class FireDeckGunEvent(TurnEvent):

    def __init__(self):
        super().__init__()
        self.game: GameStateModel = GameStateModel.instance()
        self.player = self.game.players_turn
        self.engine = self.game.game_board.engine
        self.target_tile: TileModel = NullModel()

    # TODO: Move this code to the controller for this event.
    def check(self) -> bool:
        """
        Determines whether or not it is
        possible to perform this event.

        :return: True if it possible to perform
                this event. False otherwise.
        """
        if not TurnEvent.has_required_AP(self.player.ap, 4):
            return False

        # If the player is not located in the
        # same space as the engine, they cannot
        # fire the deck gun.
        engine_orient = self.engine.orientation
        if engine_orient == VehicleOrientationEnum.HORIZONTAL:
            on_first_spot = self.player.row == self.engine.row and self.player.column == self.engine.column
            on_second_spot = self.player.row == self.engine.row and self.player.column == self.engine.column + 1
            if not on_first_spot and not on_second_spot:
                return False

        elif engine_orient == VehicleOrientationEnum.VERTICAL:
            on_first_spot = self.player.row == self.engine.row and self.player.column == self.engine.column
            on_second_spot = self.player.row == self.engine.row + 1 and self.player.column == self.engine.column
            if not on_first_spot and not on_second_spot:
                return False

        engine_quadrant = self._determine_quadrant(self.engine.row, self.engine.column)
        # If there are players present in the
        # quadrant, the deck gun cannot be fired.
        if self._are_players_in_quadrant(engine_quadrant):
            return False

        return True

    def execute(self, *args, **kwargs):
        logger.info("Executing Fire Deck Gun Event")
        self._set_target_tile()
        self.target_tile.space_status = SpaceStatusEnum.SAFE
        directions = ["North", "East", "West", "South"]
        for dirn in directions:
            has_obstacle = self.target_tile.has_obstacle_in_direction(dirn)
            obstacle = self.target_tile.get_obstacle_in_direction(dirn)
            # If there is no obstacle in the given direction or there is an
            # open door, set the status of the space in that direction to Safe.
            if not has_obstacle or (isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.OPEN):
                nb_tile: TileModel = self.target_tile.get_tile_in_direction(dirn)
                nb_tile.space_status = SpaceStatusEnum.SAFE

        self.player.ap = self.player.ap - 4

    def _set_target_tile(self):
        """
        Set the tile which will be the
        target for the firing of the deck gun.

        :return:
        """
        engine_quadrant = self._determine_quadrant(self.engine.row, self.engine.column)
        target_row = self.game.roll_red_dice()
        target_column = self.game.roll_black_dice()
        target_quadrant = self._determine_quadrant(target_row, target_column)
        # If the roll gives a tile in the engine's
        # quadrant, that will become the target tile.
        if target_quadrant == engine_quadrant:
            self.target_tile = self.game.game_board.get_tile_at(target_row, target_column)
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
                self.target_tile = self.game.game_board.get_tile_at(flipped_row, target_column)
                return

            flipped_column = self.game.determine_black_dice_opposite_face(target_column)
            new_target_quadrant = self._determine_quadrant(target_row, flipped_column)
            if new_target_quadrant == engine_quadrant:
                self.target_tile = self.game.game_board.get_tile_at(target_row, flipped_column)
                return

            new_target_quadrant = self._determine_quadrant(flipped_row, flipped_column)
            if new_target_quadrant == engine_quadrant:
                self.target_tile = self.game.game_board.get_tile_at(flipped_row, flipped_column)
                return

        # $$$$$$$$$$$$$$$$$
        # Shouldn't be able to reach this point!!
        # One of the cases above should have worked.
        # $$$$$$$$$$$$$$$$$
        logger.error("Possible issue with dice flipping! Stop!!")
        raise FlippingDiceProblemException()

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
        for player in self.game.players:
            if quadrant == self._determine_quadrant(player.row, player.column):
                return True

        return False
