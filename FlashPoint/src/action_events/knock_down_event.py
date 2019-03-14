import random
from src.action_events.action_event import ActionEvent
from src.constants.state_enums import VictimStateEnum
from src.models.game_board.null_model import NullModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.victim_model import VictimModel


class KnockDownEvent(ActionEvent):

    def __init__(self, player_ip: str):
        super().__init__()
        self.game: GameStateModel = GameStateModel.instance()
        self.player = self.game.get_player_by_ip(player_ip)

    def execute(self):
        print("Exceuting KnockDownEvent")
        # if the player was carrying a victim,
        # that victim is lost. disassociate the
        # victim from the player and increment the
        # number of victims lost.
        if isinstance(self.player.carrying_victim, VictimModel):
            self.player.carrying_victim.state = VictimStateEnum.LOST
            self.game.game_board.remove_poi_or_victim(self.player.carrying_victim)
            self.player.carrying_victim = NullModel()
            self.game.victims_lost = self.game.victims_lost + 1

        # get the closest ambulance spots to the player.
        # if there is only one closest spot, set the
        # player's location to that of the closest spot.
        # else, assign a random closest spot to the player.
        player_tile = self.game.game_board.get_tile_at(self.player.row, self.player.column)
        closest_ambulance_spots = self.game.game_board.find_closest_parking_spots("Ambulance", player_tile)
        if len(closest_ambulance_spots) == 1:
            amb_spot = closest_ambulance_spots[0]
            self.player.set_pos(amb_spot.row, amb_spot.column)

        else:
            rand_index = random.randint(0, len(closest_ambulance_spots)-1)
            amb_spot = closest_ambulance_spots[rand_index]
            self.player.set_pos(amb_spot.row, amb_spot.column)
