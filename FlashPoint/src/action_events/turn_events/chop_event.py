from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_board.wall_model import WallModel
from src.core.flashpoint_exceptions import NotEnoughAPException, WallNotAdjacent, WallAlreadyDestroyed
from src.constants.state_enums import WallStatusEnum, GameStateEnum

class ChopEvent(ActionEvent):

    def __init__(self):
        super().__init__()

    def execute(self, game: GameStateModel, fireman: PlayerModel, wall: WallModel):
        validToChop = self.can_chop(fireman)
        if not validToChop:
            raise NotEnoughAPException("chop the wall", 2)

        isPlayerAdjacent = wall.is_player_adjacent(game, fireman)
        if not isPlayerAdjacent:
            raise WallNotAdjacent(fireman.x_pos, fireman.y_pos)

        wall_status = wall.wall_status
        if wall_status == WallStatusEnum.DESTROYED:
            raise WallAlreadyDestroyed(fireman.x_pos, fireman.y_pos)

        if wall_status == WallStatusEnum.INTACT:
            wall.damage_wall()

        if wall_status == WallStatusEnum.DAMAGED:
            wall.destroy_wall()

        fireman.ap = fireman.ap - 2
        game.damage = game.damage + 1

        if game.damage == game.max_damage:
            game.game_lost()

        return


    def can_chop(self, fireman: PlayerModel) -> bool:
        if fireman.ap < 2:
            return False

        return True


