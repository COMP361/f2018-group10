from src.action_events.action_event import ActionEvent
from src.constants.change_scene_enum import ChangeSceneEnum
from src.constants.state_enums import GameStateEnum, PlayerStatusEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_state_model import GameStateModel


class EndGameEvent(ActionEvent):
    """Event to signal every client that the game has finished"""

    def __init__(self, state:GameStateEnum):
        super().__init__()
        self._state = state



    def execute(self, *args, **kwargs):

        state_model = GameStateModel.instance()
        players = state_model.players

        if self._state == GameStateEnum.LOST:
            for player in players:
                player.losses += 1
                player.status = PlayerStatusEnum.NOT_READY

            EventQueue.block()
            EventQueue.post(CustomEvent(ChangeSceneEnum.LOSESCENE))

        else:
            for player in players:
                player.wins += 1
                player.status = PlayerStatusEnum.NOT_READY

            EventQueue.block()
            EventQueue.post(CustomEvent(ChangeSceneEnum.WINSCENE))





