from src.core.custom_event import CustomEvent
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.event_queue import EventQueue
from src.action_events.action_event import ActionEvent


class StartGameEvent(ActionEvent):
    """Event to signal every client to start game."""

    def execute(self):
        EventQueue.post(CustomEvent(ChangeSceneEnum.GAMEBOARDSCENE))
