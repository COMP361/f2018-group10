import logging

from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.action_events.action_event import ActionEvent

logger = logging.getLogger("FlashPoint")


class HostDisconnectEvent(ActionEvent):
    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs):
        logger.info(f"Host has disconnected")
        EventQueue.post(CustomEvent(ChangeSceneEnum.DISCONNECT))
