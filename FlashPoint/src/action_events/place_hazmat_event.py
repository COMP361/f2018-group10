import random
import logging

from src.sprites.game_board import GameBoard
from src.sprites.hazmat_sprite import HazmatSprite
from src.models.game_units.hazmat_model import HazmatModel
from src.constants.state_enums import DifficultyLevelEnum, SpaceStatusEnum
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent

logger = logging.getLogger("FlashPoint")


class PlaceHazmatEvent(ActionEvent):

    # Constants for the number of hazmats to be placed
    RECRUIT = 3
    VETERAN = 4
    HEROIC = 5

    def __init__(self, seed: int = 0):
        super().__init__()

        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

        # Pick random location: roll dice
        random.seed(self.seed)

    def execute(self, *args, **kwargs):
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board
        """
        Place hazmat on the game board, the number of hazmats are based on the selected game mode,
        as specified in the game manual
        :param args:
        :param kwargs:
        :return:
        """
        logger.info("Executing HazMat Placement Event")
        level = self.game.difficulty_level

        if level == DifficultyLevelEnum.RECRUIT:
            self.place_hazmat(PlaceHazmatEvent.RECRUIT)

        elif level == DifficultyLevelEnum.VETERAN:
            self.place_hazmat(PlaceHazmatEvent.VETERAN)

        elif level == DifficultyLevelEnum.HEROIC:
            self.place_hazmat(PlaceHazmatEvent.HEROIC)

    def place_hazmat(self, hazmat_to_place: int):
        while hazmat_to_place > 0:
            new_haz_row = self.game.roll_red_dice()
            new_haz_column = self.game.roll_black_dice()
            tile = self.board.get_tile_at(new_haz_row, new_haz_column)

            # Hazmat cannot be placed on tile
            # that is on fire or has a hazmat
            # on it already.
            if tile.space_status == SpaceStatusEnum.FIRE:
                continue

            should_reroll = False
            for model in tile.associated_models:
                if isinstance(model, HazmatModel):
                    should_reroll = True
                    break

            if should_reroll:
                continue

            tile.add_associated_model(HazmatModel())
            GameBoard.instance().add(HazmatSprite(tile))
            hazmat_to_place -= 1
