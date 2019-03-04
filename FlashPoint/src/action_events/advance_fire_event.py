from src.action_events.action_event import ActionEvent
from src.action_events.turn_events.knock_down_event import KnockDownEvent
from src.constants.state_enums import SpaceStatusEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units import player_model
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class AdvanceFireEvent(ActionEvent):

    def __init__(self):
        super().__init__()
        self.game_state = GameStateModel.instance()
        self.board = self.game_state.gameboard()
        self.initial_tile = None
        self._red_dice = None
        self._black_dice = None

    def execute(self, *args, **kwargs):
        # Pick random location
        if not self._red_dice:
            # roll dice
            self._red_dice = self.game_state.roll_red_dice()
        if not self._black_dice:
            self._black_dice = self.game_state.roll_black_dice()
        # next step is to determine what that tile conatins.
        self.get_tile()
        self.check_associated_models()
        status = self.initial_tile.space_status()
        if status is SpaceStatusEnum.SAFE or status is SpaceStatusEnum.SMOKE:
            self.initial_tile.set_status(SpaceStatusEnum.FIRE)

        elif status is SpaceStatusEnum.FIRE:
            self.explosion()

    def get_tile(self):
        self.initial_tile = self.board.get_tile_at(self._red_dice,
                                                   self._black_dice)  # gets starting tile of advance fire.

    def explosion(self):
        pass

    def check_associated_models(self):
        assoc_models = self.initial_tile.associated_models()
        for model in assoc_models:
            if isinstance(player_model, model):
                KnockDownEvent(model).execute()
            if isinstance(VictimModel, model):
                victim_lost = self.game_state.victims_lost()
                self.game_state.victims_lost(victim_lost + 1)
                model.set_dead()

            if isinstance(POIModel, model):
                model.reveal()
