from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel
import random


class SetInitialPOIFamilyEvent(ActionEvent):

    def __init__(self, seed: int = 0):
        super().__init__()
        self.game_state: GameStateModel = GameStateModel.instance()
        if seed == 0:
            self.seed = random.randint(0, 6969)
        else:
            self.seed = seed

        self.rand_nums = random.sample(range(0, len(self.game_state.game_board.poi_bank)), 3)

    def execute(self, *args, **kwargs):
        """
        Set active POI's and their positions for a family game.
        Set all initial POIlocations for a family game.
        Returns the locations that were randomly chosen for reuse in the PlacePOIEvent
        """
        locations = [[2, 4], [5, 1], [5, 8]]
        for i, index in enumerate(self.rand_nums):
            poi = self.game_state.game_board.get_poi_from_bank_by_index(index)
            row = locations[i][0]
            column = locations[i][1]
            poi.set_pos(row, column)
            self.game_state.game_board.active_pois.append(poi)
            self.game_state.game_board.remove_from_poi_bank(poi)
            self.game_state.game_board.get_tile_at(row, column).add_associated_model(poi)
