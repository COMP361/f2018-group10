from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel


class GameBoardState(object):
    pass


class EndTurnEvent(ActionEvent):

    def __init__(self):
        super().__init__()

    def execute(self):
        GameStateModel.instance().next_player()
        """
        1)
        2)start the AdvanceFire
        3)knockdown event
        4)replenish POI
        5)call player_next
        :return:
        """


