from src.action_events.action_event import ActionEvent
from src.constants.state_enums import PlayerStatusEnum, VictimStateEnum
from src.models.game_board.null_model import NullModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel

# TODO: resolve knock down. Please refer to M5 models to save some time on this:
# Player status = KnockedDown
# Player location = Nearest Ambulance
#
from src.models.game_units.victim_model import VictimModel


class KnockDownEvent(ActionEvent):

    def __init__(self, player: PlayerModel):
        super().__init__()
        self.player = player
        self.game: GameStateModel = GameStateModel.instance()

    def execute(self):
        # if the player was carrying a victim,
        # that victim is lost. disassociate the
        # victim from the player and increment the
        # number of victims lost.
        if isinstance(self.player.carrying_victim, VictimModel):
            self.player.carrying_victim.state = VictimStateEnum.LOST
            self.player.carrying_victim = NullModel()
            self.game.victims_lost += 1

        # get the closest ambulance spots to the player.
        # if there is only one closest spot, set the
        # player's location to that of the closest spot.
        # else, offer the user a choice from the list of
        # closest spots available.
        player_tile = self.game.game_board.get_tile_at(self.player.row, self.player.column)
        closest_ambulance_spots = self.game.game_board.find_closest_parking_spots("Ambulance", player_tile)
        if len(closest_ambulance_spots) == 1:
            amb_spot = closest_ambulance_spots[0]
            self.player.row = amb_spot.row
            self.player.column = amb_spot.column

        else:
            # TODO: how to handle choice for more than one closest spots?
            pass
