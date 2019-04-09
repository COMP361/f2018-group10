from src.action_events.action_event import ActionEvent


class TooManyPlayersEvent(ActionEvent):
    """
    Doesn't do anything, this gets sent by the host to the client when the lobby is full
    """
    def execute(self):
        pass
