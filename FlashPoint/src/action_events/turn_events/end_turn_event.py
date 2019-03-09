from src.constants.state_enums import GameStateEnum
from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel


class GameBoardState(object):
    pass


class EndTurnEvent(ActionEvent):

    def __init__(self):
        super().__init__()

    def execute(self):
        # for testing
        # GameStateModel.instance().damage = 5
        # GameStateModel.instance().players_turn.ap =  GameStateModel.instance().players_turn.ap + 4
        GameStateModel.instance().next_player()
        """
        1)
        2)start the AdvanceFire
        3)knockdown event
        4)replenish POI
        5)call player_next
        :return:
        """


