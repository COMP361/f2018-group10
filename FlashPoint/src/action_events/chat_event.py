import logging

from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent

logger = logging.getLogger("FlashPoint")


class ChatEvent(ActionEvent):
    """Class representing how to update a games chathistory so that players can chat."""

    def __init__(self, message: str, sender_nickname: str):
        super().__init__()
        self._sender = sender_nickname
        self._message = message

    def execute(self):
        logger.info("Executing ChatEvent")
        GameStateModel.instance().add_chat_message(self._message, self._sender)
