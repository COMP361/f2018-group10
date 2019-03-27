import random

from src.models.game_units.victim_model import VictimModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.hazmat_model import HazmatModel
from src.constants.state_enums import DifficultyLevelEnum, SpaceStatusEnum
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent


class PlaceHazmatEvent(ActionEvent):

    # Constants for the number of hazmats to be placed
    RECRUIT = 3
    VETERAN = 4
    HEROIC = 5

    def __init__(self, seed: int = 0):
        super().__init__()
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board

        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

        # Pick random location: roll dice
        random.seed(self.seed)

    def execute(self, *args, **kwargs):
        """
        Place hazmat on the game board, the number of hazmats are based on the selected game mode,
        as specified in the game manual
        :param args:
        :param kwargs:
        :return:
        """
        level = self.game.difficulty_level

        if level is DifficultyLevelEnum.RECRUIT:
            self.place_hazmat(self.RECRUIT)

        elif level is DifficultyLevelEnum.VETERAN:
            self.place_hazmat(self.VETERAN)

        elif level is DifficultyLevelEnum.HEROIC:
            self.place_hazmat(self.HEROIC)

    def place_hazmat(self, hazmat_to_place: int):
        while hazmat_to_place > 0:
            new_haz_row = self.game.roll_red_dice()
            new_haz_column = self.game.roll_black_dice()
            tile = self.board.get_tile_at(new_haz_row, new_haz_column)

            if tile.space_status is not SpaceStatusEnum.SAFE:
                continue

            for model in tile.associated_models:
                if isinstance(model, HazmatModel) or isinstance(model, POIModel) or isinstance(model, VictimModel):
                    continue

            print(f"Placed hazmat on location: {new_haz_row}, {new_haz_column}")
            tile.add_associated_model(HazmatModel())
            hazmat_to_place -= 1
