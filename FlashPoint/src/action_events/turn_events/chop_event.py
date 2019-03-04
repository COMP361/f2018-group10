from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_board.wall_model import WallModel
from src.core.flashpoint_exceptions import NotEnoughAPException, WallNotAdjacent, WallAlreadyDestroyed
from src.constants.state_enums import WallStatusEnum


class ChopEvent(TurnEvent):

    def __init__(self):
        super().__init__()

    def execute(self, fireman: PlayerModel, wall: WallModel):
        # TODO: Start here - This is the precondition code - Move it to the GUI
        game = GameStateModel.instance()
        valid_to_chop = self.has_required_AP(fireman.ap, 2)
        if not valid_to_chop:
            raise NotEnoughAPException("chop the wall", 2)

        player_tile = game.game_board.get_tile_at(fireman.x_pos, fireman.y_pos)

        if wall not in player_tile.adjacent_edge_objects:
            raise WallNotAdjacent(fireman.x_pos, fireman.y_pos)

        wall_status = wall.wall_status
        if wall_status == WallStatusEnum.DESTROYED:
            raise WallAlreadyDestroyed(fireman.x_pos, fireman.y_pos)
        # End here

        if wall_status == WallStatusEnum.INTACT:
            wall.damage_wall()

        if wall_status == WallStatusEnum.DAMAGED:
            wall.destroy_wall()

        fireman.ap = fireman.ap - 2
        game.damage = game.damage + 1

        if game.damage == game.max_damage:
            game.game_lost()

        return
