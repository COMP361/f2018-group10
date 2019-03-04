from src.core.networking import Networking
from src.action_events.action_event import ActionEvent


class StartGameEvent(ActionEvent):
    """Event to signal every client to start game."""

    def execute(self):
        Networking.get_instance().start_game()
