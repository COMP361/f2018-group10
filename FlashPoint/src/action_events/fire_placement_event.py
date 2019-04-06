import logging
import random
from typing import Tuple

from src.action_events.end_turn_advance_fire import EndTurnAdvanceFireEvent
from src.constants.state_enums import GameKindEnum, SpaceStatusEnum, DifficultyLevelEnum
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent

logger = logging.getLogger("FlashPoint")


class FirePlacementEvent(ActionEvent):
    """Event for placing fires at the beginning of the game."""

    def __init__(self, seed: int = 0):
        super().__init__()
        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

        # Pick random location: roll dice
        random.seed(self.seed)

    def execute(self):
        logger.info("Executing Fire Placement Event")
        if GameStateModel.instance().rules == GameKindEnum.FAMILY:
            GameStateModel.instance().game_board.set_fires_family()
        else:
            self._set_fires_heroic_veteran_recruit(GameStateModel.instance().difficulty_level)

    def _set_fires_heroic_veteran_recruit(self, difficulty_lvl: DifficultyLevelEnum):
        advance_event = EndTurnAdvanceFireEvent()
        # First explosion:
        # Roll the black dice to determine where the
        # first explosion will take place. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        logger.info("First explosion")
        tile_pos = self._first_explosion_dice_roll()
        tile = GameStateModel.instance().game_board.get_tile_at(tile_pos[0], tile_pos[1])
        self._perform_fire_hotspot_explosion(tile, advance_event)

        # Second explosion:
        # Roll both dice to determine the target space. Keep rolling
        # until you get a non-fire space. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        logger.info("Second explosion")
        tile_pos = [GameStateModel.instance().roll_red_dice(), GameStateModel.instance().roll_black_dice()]
        while GameStateModel.instance().game_board.get_tile_at(tile_pos[0], tile_pos[1]).space_status == SpaceStatusEnum.FIRE:
            tile_pos = [GameStateModel.instance().roll_red_dice(), GameStateModel.instance().roll_black_dice()]

        tile = GameStateModel.instance().game_board.get_tile_at(tile_pos[0], tile_pos[1])
        self._perform_fire_hotspot_explosion(tile, advance_event)

        # Third explosion:
        # Flip over the black dice from the previous roll to get
        # the new column. Roll the red dice. Keep rolling until you
        # get a non-fire space. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        logger.info("Third explosion")
        column = GameStateModel.instance().determine_black_dice_opposite_face(tile_pos[1])
        tile_pos = [GameStateModel.instance().roll_red_dice(), column]
        while GameStateModel.instance().game_board.get_tile_at(tile_pos[0], tile_pos[1]).space_status == SpaceStatusEnum.FIRE:
            tile_pos = [GameStateModel.instance().roll_red_dice(), column]

        tile = GameStateModel.instance().game_board.get_tile_at(tile_pos[0], tile_pos[1])
        self._perform_fire_hotspot_explosion(tile, advance_event)

        # Conditional fourth explosion:
        # Only happens if playing at the Heroic level. Roll both
        # dice to determine target space. Keep rolling until you
        # get a non-fire space. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        if difficulty_lvl == DifficultyLevelEnum.HEROIC:
            logger.info("Fourth explosion")
            tile_pos = [GameStateModel.instance().roll_red_dice(), GameStateModel.instance().roll_black_dice()]
            while GameStateModel.instance().game_board.get_tile_at(tile_pos[0], tile_pos[1]).space_status == SpaceStatusEnum.FIRE:
                tile_pos = [GameStateModel.instance().roll_red_dice(), GameStateModel.instance().roll_black_dice()]

            tile = GameStateModel.instance().game_board.get_tile_at(tile_pos[0], tile_pos[1])
            self._perform_fire_hotspot_explosion(tile, advance_event)

    def _perform_fire_hotspot_explosion(self, tile: TileModel, advance_event: EndTurnAdvanceFireEvent):
        """
        Set the tile on fire, turn hotspot to true and
        cause an explosion on that tile.

        :param tile: Target tile
        :param advance_event: Advance event to access explosion
        :return:
        """
        tile.space_status = SpaceStatusEnum.FIRE
        tile.is_hotspot = True
        advance_event.explosion(tile)

    def _first_explosion_dice_roll(self) -> Tuple[int, int]:
        """
        Rolling the black dice to determine the
        location of the first explosion.

        :return: Location of first explosion
        """
        roll = GameStateModel.instance().roll_black_dice()
        if roll == 1:
            return 3, 3

        elif roll == 2:
            return 3, 4

        elif roll == 3:
            return 3, 5

        elif roll == 4:
            return 3, 6

        elif roll == 5:
            return 4, 6

        elif roll == 6:
            return 4, 5

        elif roll == 7:
            return 4, 4

        elif roll == 8:
            return 4, 3
