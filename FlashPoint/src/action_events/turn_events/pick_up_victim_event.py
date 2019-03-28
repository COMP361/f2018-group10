import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")


class PickupVictimEvent(TurnEvent):

    def __init__(self, victim: VictimModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        print(f"{victim.row}, {victim.column}")
        self.victim_tile = game.game_board.get_tile_at(victim.row, victim.column)
        for assoc_model in self.victim_tile.associated_models:
            if isinstance(assoc_model, VictimModel):
                self.victim = assoc_model
                break

        self.player: PlayerModel = game.players_turn

    def execute(self):
        logger.info("Excecuting PickupVictimEvent")
        self.player.carrying_victim = self.victim
        self.victim_tile.remove_associated_model(self.victim_tile)
