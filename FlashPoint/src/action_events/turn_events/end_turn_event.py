from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class EndTurnEvent(TurnEvent):

    def __init__(self, player: PlayerModel):
        super().__init__()
        self.player = GameStateModel.instance().players_turn

    def execute(self):
        """
        Steps:
        1)start the AdvanceFire
        2)knockdown event
        3)replenish POI
        4)retain and replenish player's AP
        5)call player_next
        :return:
        """
        # retain upto a maximum of 4 AP
        # as the turn is ending and
        # replenish player's AP by 4
        GameStateModel.lock.acquire()
        if self.player.ap > 4:
            self.player.ap = 4

        self.player.ap += 4

        # call next player
        GameStateModel.instance().next_player()
        GameStateModel.lock.release()
