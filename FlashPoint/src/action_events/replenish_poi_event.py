import logging
import random

from src.models.game_board.tile_model import TileModel
from src.core.flashpoint_exceptions import NoAvailableTileException
from src.action_events.action_event import ActionEvent
from src.constants.state_enums import SpaceStatusEnum, POIIdentityEnum, VictimStateEnum, GameKindEnum, \
    ArrowDirectionEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")


class ReplenishPOIEvent(ActionEvent):

    def __init__(self, seed: int = 0):
        super().__init__()
        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

        # Pick random location: roll dice
        random.seed(self.seed)
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board

    # Use this method to check whether
    # the POIs should be replenished or not
    def check(self):
        num_active_pois = len(self.board.active_pois)
        logger.info(f"There are currently {num_active_pois} active poi's")
        if num_active_pois >= 3:
            return False

        return True

    def execute(self):
        print()
        logger.info("Executing ReplenishPOIEvent")
        if not self.check():
            logger.info("There are more than 3 poi's active, don't need to replenish.")
            return

        num_pois_to_add = 3 - len(self.board.active_pois)
        logger.info(f"Must add {num_pois_to_add} poi's")
        logger.info(f"There are {len(self.board.poi_bank)} pois left in the bank.")

        should_roll = num_pois_to_add > 0 and len(self.board.poi_bank) > 0

        while should_roll:
            new_poi_row = self.game.roll_red_dice()
            new_poi_column = self.game.roll_black_dice()
            new_poi = self.board.get_random_poi_from_bank()

            if self.game.rules is GameKindEnum.FAMILY:
                new_poi.set_pos(new_poi_row, new_poi_column)
                tile = self.board.get_tile_at(new_poi_row, new_poi_column)

                logger.info(f"Attempting to place new poi on location: {new_poi_row}, {new_poi_column}")
                if tile.has_poi_or_victim():
                    logger.info("Tile has poi or victim, will reroll")
                    should_roll = True
                    continue

                if tile.space_status != SpaceStatusEnum.SAFE:
                    logger.info("Tile was not SAFE for adding POI. It is now safe.")
                    tile.space_status = SpaceStatusEnum.SAFE

            else:
                try:
                    (new_poi_row, new_poi_column) = self.check_arrow_path(new_poi_row, new_poi_column)
                    new_poi.set_pos(new_poi_row, new_poi_column)
                    tile = self.board.get_tile_at(new_poi_row, new_poi_column)
                except NoAvailableTileException:
                    should_roll = True
                    continue

            if self.game.get_players_on_tile(tile.row, tile.column):
                if new_poi.identity == POIIdentityEnum.FALSE_ALARM:
                    should_roll = True
                    continue
                else:
                    new_victim = VictimModel(VictimStateEnum.ON_BOARD)
                    new_victim.set_pos(new_poi_row, new_poi_column)
                    tile.add_associated_model(new_victim)
                    self.board.add_poi_or_victim(new_victim)
                    new_poi.reveal(new_victim)

            tile.add_associated_model(new_poi)
            self.board.add_poi_or_victim(new_poi)
            self.board.poi_bank.remove(new_poi)
            num_pois_to_add = 3 - len(self.board.active_pois)
            should_roll = num_pois_to_add > 0 and len(self.board.poi_bank) > 0

    def check_arrow_path(self, row: int, column: int) -> (int, int):
        """
        Gets the next tile following the arrow path, raises a NoAvailableTileException if no available tile can be found
        (ie. the loop goes back to the original point)
        :param row:
        :param column:
        :return:
        """
        logger.info(f"Attempting to place new poi on location: {row}, {column}")
        if self.place_check_experienced(row, column):
            return row, column

        (row_ptr, column_ptr) = self.get_next_tile(row, column)

        while (row_ptr, column_ptr) != (row, column):
            logger.info(f"Attempting to place new poi on location: {row_ptr}, {column_ptr}")
            if self.place_check_experienced(row_ptr, column_ptr):
                return row_ptr, column_ptr
            else:
                (row_ptr, column_ptr) = self.get_next_tile(row_ptr, column_ptr)

        raise NoAvailableTileException

    def place_check_experienced(self, row: int, column: int) -> bool:
        tile: TileModel = self.board.get_tile_at(row, column)

        if tile.space_status is not SpaceStatusEnum.SAFE:
            logger.info("Tile is not SAFE, will check the next arrow path")
            return False

        if tile.has_poi_or_victim():
            logger.info("Tile has poi or victim, will check the next arrow path")
            return False

        for player in self.game.players:
            if (player.row is row) and (player.column is column):
                logger.info("Found a player at the same tile, will check the next arrow path")
                return False

        return True

    def get_next_tile(self, row: int, column: int) -> (int, int):
        tile: TileModel = self.board.get_tile_at(row, column)
        logger.info(f"Next tile at direction: {tile.arrow_dirn}")

        if tile.arrow_dirn is ArrowDirectionEnum.NORTH:
            dest: TileModel = tile.north_tile
            return dest.row, dest.column

        elif tile.arrow_dirn is ArrowDirectionEnum.EAST:
            dest: TileModel = tile.east_tile
            return dest.row, dest.column

        elif tile.arrow_dirn is ArrowDirectionEnum.WEST:
            dest: TileModel = tile.west_tile
            return dest.row, dest.column

        elif tile.arrow_dirn is ArrowDirectionEnum.SOUTH:
            dest: TileModel = tile.south_tile
            return dest.row, dest.column

        elif tile.arrow_dirn is ArrowDirectionEnum.NORTH_EAST:
            dest: TileModel = tile.east_tile.north_tile
            return dest.row, dest.column

        elif tile.arrow_dirn is ArrowDirectionEnum.NORTH_WEST:
            dest: TileModel = tile.west_tile.north_tile
            return dest.row, dest.column

        elif tile.arrow_dirn is ArrowDirectionEnum.SOUTH_EAST:
            dest: TileModel = tile.east_tile.south_tile
            return dest.row, dest.column

        elif tile.arrow_dirn is ArrowDirectionEnum.SOUTH_WEST:
            dest: TileModel = tile.west_tile.south_tile
            return dest.row, dest.column
