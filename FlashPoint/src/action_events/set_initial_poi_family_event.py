import logging

from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel
import random

logger = logging.getLogger("FlashPoint")


class SetInitialPOIFamilyEvent(ActionEvent):

    def __init__(self, seed: int = 0):
        super().__init__()
        self.game_state: GameStateModel = GameStateModel.instance()
        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

        random.seed(self.seed)
        self.rand_nums = random.sample(range(len(self.game_state.game_board.poi_bank)), 3)

    def execute(self, *args, **kwargs):
        """
        Set active POI's and their positions for a family game.
        Set all initial POIlocations for a family game.
        Returns the locations that were randomly chosen for reuse in the PlacePOIEvent
        """
        logging.info("Executing Set Initial POI Family Event")
        locations = [[2, 4], [5, 1], [5, 8]]
        pois_to_remove = []
        for i, index in enumerate(self.rand_nums):
            poi = self.game_state.game_board.get_poi_from_bank_by_index(index)
            row = locations[i][0]
            column = locations[i][1]
            self.game_state.game_board.add_poi_or_victim(poi)
            self.game_state.game_board.get_tile_at(row, column).add_associated_model(poi)
            pois_to_remove.append(poi)

        for poi in pois_to_remove:
            self.game_state.game_board.remove_from_poi_bank(poi)
