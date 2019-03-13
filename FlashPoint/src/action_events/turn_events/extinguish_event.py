from src.core.event_queue import EventQueue
from src.sprites.game_board import GameBoard
from src.sprites.tile_sprite import TileSprite
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import SpaceStatusEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class ExtinguishEvent(TurnEvent):

    def __init__(self, extinguish_space: TileModel):
        super().__init__()
        self.fireman: PlayerModel = GameStateModel.instance().players_turn
        self.extinguish_space: TileModel = extinguish_space

    def execute(self):
        fireman = self.fireman
        extinguish_space = self.extinguish_space
        # tile_sprite: TileSprite = GameBoard.instance().grid.grid[extinguish_space.column][extinguish_space.row]

        if extinguish_space.space_status == SpaceStatusEnum.SMOKE:
            extinguish_space.space_status = SpaceStatusEnum.SAFE

        elif extinguish_space.space_status == SpaceStatusEnum.FIRE:
            extinguish_space.space_status = SpaceStatusEnum.SMOKE

        else:
            return

        fireman.ap = fireman.ap - 1

        print(extinguish_space)
        return
