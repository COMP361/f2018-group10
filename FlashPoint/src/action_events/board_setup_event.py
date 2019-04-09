import random
import time

from src.action_events.action_event import ActionEvent
from src.action_events.fire_placement_event import FirePlacementEvent
from src.action_events.place_hazmat_event import PlaceHazmatEvent
from src.action_events.set_initial_hotspot_event import SetInitialHotspotEvent
from src.action_events.set_initial_poi_experienced_event import SetInitialPOIExperiencedEvent
from src.action_events.set_initial_poi_family_event import SetInitialPOIFamilyEvent
from src.constants.state_enums import GameKindEnum
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard


class BoardSetupEvent(ActionEvent):
    """Group the board setup events together since they need to execute in a particular order."""

    def __init__(self, seed=0):
        super().__init__()

        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

        # Pick random location: roll dice
        random.seed(self.seed)

    def execute(self, *args, **kwargs):
        while not GameBoard.instance():
            time.sleep(0.1)
        FirePlacementEvent(self.seed).execute()

        if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
            SetInitialPOIExperiencedEvent(self.seed).execute()
            PlaceHazmatEvent(self.seed).execute()
            SetInitialHotspotEvent(self.seed).execute()
        else:
            SetInitialPOIFamilyEvent().execute()
