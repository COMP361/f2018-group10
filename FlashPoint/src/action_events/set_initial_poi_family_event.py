from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel
import random


class SetInitialPOIFamilyEvent(ActionEvent):

    def __init__(self, random_number1: int = None, random_number2: int = None, random_number3: int = None):
        super().__init__()
        self.game_state: GameStateModel = GameStateModel.instance()
        self.random_num1 = random_number1
        self.random_num2 = random_number2
        self.random_num3 = random_number3
        l = set(i for i in range(10))

        if not self.random_num1:
            self.random_num1 = random.randint(0, len(l)-1)

        if not self.random_num2:
            while True:
                num = random.randint(0, len(l) - 1)
                self.random_num2 = num
                if num != self.random_num1:
                    break

        if not self.random_num3:
            while True:
                num = random.randint(0, len(l) - 1)
                self.random_num3 = num
                if num != self.random_num1 and num != self.random_num2:
                    break

    def execute(self, *args, **kwargs):
        """
        Set active POI's and their positions for a family game.
        Set all initial POIlocations for a family game.
        Returns the locations that were randomly chosen for reuse in the PlacePOIEvent
        """
        locations = [[2, 4], [5, 1], [5, 8]]
        for i, index in enumerate([self.random_num1, self.random_num2, self.random_num3]):
            poi = self.game_state.game_board.get_poi_from_bank_by_index(index)
            row = locations[i][0]
            column = locations[i][1]
            poi.set_pos(row, column)
            self.game_state.game_board.active_pois.append(poi)
            self.game_state.game_board.get_tile_at(row, column).add_associated_model(poi)
        poi1 = self.game_state.game_board.get_poi_from_bank_by_index(self.random_num1)
        poi2 = self.game_state.game_board.get_poi_from_bank_by_index(self.random_num2)
        poi3 = self.game_state.game_board.get_poi_from_bank_by_index(self.random_num3)
        self.game_state.game_board.remove_from_poi_bank(poi1)
        self.game_state.game_board.remove_from_poi_bank(poi2)
        self.game_state.game_board.remove_from_poi_bank(poi3)
