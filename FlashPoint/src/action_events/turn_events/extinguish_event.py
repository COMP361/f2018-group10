from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import SpaceStatusEnum
from src.core.flashpoint_exceptions import ModelNotAdjacent, NotEnoughAPException
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class ExtinguishEvent(TurnEvent):

    def __init__(self):
        super().__init__()

    def execute(self, fireman: PlayerModel, extinguish_space: TileModel):
        game: GameStateModel = GameStateModel.instance()
        # TODO: Start here - This is the precondition code - Move it to the GUI
        player_tile = game.game_board.get_tile_at(fireman.x_pos, fireman.y_pos)
        valid_to_extinguish = extinguish_space == player_tile or extinguish_space in player_tile.adjacent_tiles
        if not valid_to_extinguish:
            raise ModelNotAdjacent("tile", fireman.x_pos, fireman.y_pos)

        if not self.has_required_AP(fireman.ap, 1):
            raise NotEnoughAPException("extinguish", 1)

        # TODO: End here
        if extinguish_space.space_status == SpaceStatusEnum.SMOKE:
            extinguish_space.space_status = SpaceStatusEnum.SAFE

        elif extinguish_space.space_status == SpaceStatusEnum.FIRE:
            extinguish_space.space_status = SpaceStatusEnum.SMOKE

        else:
            return

        fireman.ap = fireman.ap - 1
        return
