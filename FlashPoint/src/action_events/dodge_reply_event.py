import src.core.pause_event_switch as switch
from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel


class DodgeReplyEvent(ActionEvent):

    def __init__(self, reply: bool):
        super().__init__()
        self._reply = reply

    def execute(self, *args, **kwargs):
        """Unblock the waiting thread."""
        GameStateModel.instance().dodge_reply = self._reply
        switch.pause_event.set()
