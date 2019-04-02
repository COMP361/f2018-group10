import logging
import random

from src.action_events.action_event import ActionEvent
from src.constants.state_enums import SpaceStatusEnum, POIIdentityEnum, VictimStateEnum
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
            new_poi.set_pos(new_poi_row, new_poi_column)
            tile = self.board.get_tile_at(new_poi_row, new_poi_column)

            logger.info(f"Attempting to place new poi on location: {new_poi_row}, {new_poi_column}")
            if tile.has_poi_or_victim():
                should_roll = True
                continue

            if tile.space_status != SpaceStatusEnum.SAFE:
                logger.info("Tile was not SAFE for adding POI. It is now safe.")
                tile.space_status = SpaceStatusEnum.SAFE

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
