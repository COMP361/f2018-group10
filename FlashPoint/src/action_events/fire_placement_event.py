from src.constants.state_enums import GameKindEnum
from src.models.game_state_model import GameStateModel
from src.action_events.turn_events.turn_event import TurnEvent


class FirePlacementEvent(TurnEvent):
    """Event for placing fires at the beginning of the game."""

    def __init__(self):
        super().__init__()

    def execute(self, game: GameStateModel):
        if game.difficulty_level == GameKindEnum.FAMILY:
            game.game_board.set_fires_family()
