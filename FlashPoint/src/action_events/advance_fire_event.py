from src.models.game_state_model import GameStateModel


class AdvanceFireEvent(ActionEvent):

    def __init__(self):
        self._red_dice = None
        self._black_dice = None

    def execute(self, *args, **kwargs):
        # Pick random location
        if not self._red_dice:
            # roll dice
            self._red_dice = GameStateModel.instance().roll_red_dice()
        if not self._black_dice:
            self._black_dice = GameStateModel.instance().roll_black_dice()
