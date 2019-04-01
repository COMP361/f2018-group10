import logging

from src.models.game_state_model import GameStateModel
from src.constants.state_enums import GameStateEnum
from src.core.custom_event import CustomEvent
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.event_queue import EventQueue
from src.action_events.action_event import ActionEvent

logging.getLogger("FlashPoint")


class StartGameEvent(ActionEvent):
    """Event to signal every client to start game."""

    def execute(self):
        logging.info("Executing StartGameEvent.")
        GameStateModel.instance().state = GameStateEnum.PLACING_PLAYERS
        EventQueue.block()
        EventQueue.post(CustomEvent(ChangeSceneEnum.GAMEBOARDSCENE))
