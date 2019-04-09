import logging
import random
from typing import List

from src.action_events.action_event import ActionEvent
from src.constants.state_enums import SpaceStatusEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.poi_model import POIModel

logger = logging.getLogger("FlashPoint")


class SetInitialPOIExperiencedEvent(ActionEvent):

    def __init__(self, seed: int = 0):
        super().__init__()
        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

    def execute(self, *args, **kwargs):
        """
        Set the initial POIs for the experienced
        game by rolling the dice three times.

        :param args:
        :param kwargs:
        :return:
        """
        self.game: GameStateModel = GameStateModel.instance()
        self.game_board = self.game.game_board
        # Pick random location: roll dice
        random.seed(self.seed)
        self.rand_nums = random.sample(range(len(self.game_board.poi_bank)), 3)
        logging.info("Executing Set Initial POI Experienced Event")

        pois_to_remove = []
        pois_placed = 0
        for index in self.rand_nums:
            reroll = True
            while reroll:
                reroll = False
                row = self.game.roll_red_dice()
                column = self.game.roll_black_dice()
                target_tile = self.game_board.get_tile_at(row, column)

                for assoc_model in target_tile.associated_models:
                    if isinstance(assoc_model, POIModel):
                        reroll = True

                if target_tile.space_status == SpaceStatusEnum.FIRE:
                    reroll = True

            poi = self.game_board.get_poi_from_bank_by_index(index)
            self.game_board.add_poi_or_victim(poi)
            self.game_board.get_tile_at(row, column).add_associated_model(poi)
            pois_to_remove.append(poi)

            pois_placed += 1

        for poi in pois_to_remove:
            self.game_board.remove_from_poi_bank(poi)

    def _determine_locations(self) -> List[List[int]]:
        """
        Determines the locations
        where the POI will be placed

        :return: List of valid coordinates
        """
        num_locations = 0
        locations = []
        while num_locations < 3:
            row = self.game.roll_red_dice()
            column = self.game.roll_black_dice()
            target_tile = self.game_board.get_tile_at(row, column)
            contains_poi = False
            for assoc_model in target_tile.associated_models:
                if isinstance(assoc_model, POIModel):
                    contains_poi = True
                    break

            # If the tile already contains a POI or
            # it is on fire, we cannot place a POI here.
            if contains_poi:
                continue

            if target_tile.space_status == SpaceStatusEnum.FIRE:
                continue

            locations.append([row, column])
            num_locations += 1

        return locations
