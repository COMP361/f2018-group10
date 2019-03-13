from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.victim_model import VictimModel


class PickupVictimEvent(TurnEvent):

    def __init__(self, victim: VictimModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.victim_tile = game.game_board.get_tile_at(victim.row, victim.column)
        for assoc_model in self.victim_tile.associated_models:
            if isinstance(assoc_model, VictimModel):
                self.victim = assoc_model
                break

        self.player = game.players_turn

    #### Use this check in the GUI to determine
    #### whether or not to show a pick up victim option


    def execute(self):
        self.player.carrying_victim = self.victim
        self.victim_tile.remove_associated_model(self.victim)
