from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import SpaceStatusEnum
from src.core.flashpoint_exceptions import ModelNotAdjacentException, NotEnoughAPException
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_board.game_board_model import GameBoardModel


class ExtinguishEvent(TurnEvent):

    def __init__(self, extinguish_space: TileModel):
        super().__init__()
        self.fireman: PlayerModel = GameStateModel.instance().players_turn
        self.extinguish_space: TileModel = extinguish_space

    def execute(self):
        fireman = self.fireman
        extinguish_space = self.extinguish_space

        if extinguish_space.space_status == SpaceStatusEnum.SMOKE:
            extinguish_space.space_status = SpaceStatusEnum.SAFE

        elif extinguish_space.space_status == SpaceStatusEnum.FIRE:
            extinguish_space.space_status = SpaceStatusEnum.SMOKE

        else:
            return

        fireman.ap = fireman.ap - 1
        return
