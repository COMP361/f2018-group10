from abc import ABC, abstractmethod


class ActionEvent(ABC):
    """Abstract base class for all ActionEvent types. Should contain all information needed to
        update game state on remote clients.


        Tips for creating events:

        -Only pass what you absolutely need as params to the constructor. Any object that you use will need to be
         serialized (and deserialized). If we don't already have a method of deserializing that object, you'll have to
         add one. So if you can avoid it, please do!

        -Don't save the "current player". Use the GamestateModel.instance().players_turn instead.

        -Events should not directly use the Networking class.

        -Events should not have any logic for "validating" that the action was correct. The GUI controllers do that.

        -Keep in mind that Events get executed only AFTER being sent over the network to all clients and deserialized.

        -You'll need to write a deserialize method in the serializer.py file for this event to work.

        """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
