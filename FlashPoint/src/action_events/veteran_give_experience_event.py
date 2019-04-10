import logging

from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel

logger = logging.getLogger("FlashPoint")

class VeteranGiveExperienceEvent(ActionEvent):

    def __init__(self, player: PlayerModel, player_booleans: dict):
        super().__init__()
        self.c_player = [p for p in GameStateModel.instance().players if player == p][0]
        self.player_booleans = player_booleans

    def execute(self, *args, **kwargs):
        """
        Give 1 free AP to the CURRENT player
        in the vicinity of the Veteran if applicable.
        Give the dodge ability to ALL the players
        in the vicinity of the Veteran if applicable,
        else take that ability away.

        :return:
        """
        logger.info("Executing Veteran Give Experience Event")
        self.game: GameStateModel = GameStateModel.instance()
        for ip, can_dodge in self.player_booleans.items():
            player = self.game.get_player_by_ip(ip)
            player.allowed_to_dodge = can_dodge
            if player == self.c_player:
                if not player.has_AP_from_veteran:
                    player.ap = player.ap + 1
                    player.has_AP_from_veteran = True
