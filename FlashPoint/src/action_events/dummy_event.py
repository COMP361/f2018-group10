from src.action_events.action_event import ActionEvent


class DummyEvent(ActionEvent):
    """
    Doesn't do anything, this gets sent by the clients to the host to say: "Hey I'm still here"
    If the host detects that they are no longer receiving events from a client they will drop the connection.
    """
    def execute(self):
        pass
