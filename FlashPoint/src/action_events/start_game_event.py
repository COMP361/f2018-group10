import time
from src.models.game_state_model import GameStateModel
from src.constants.state_enums import GameStateEnum
from src.core.custom_event import CustomEvent
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.event_queue import EventQueue
from src.action_events.action_event import ActionEvent


class StartGameEvent(ActionEvent):
    """Event to signal every client to start game."""

    def execute(self):
        GameStateModel.instance().state = GameStateEnum.PLACING_PLAYERS
        time.sleep(0.1)
        EventQueue.block()
        EventQueue.post(CustomEvent(ChangeSceneEnum.GAMEBOARDSCENE))