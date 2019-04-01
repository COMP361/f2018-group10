import logging

from src.action_events.action_event import ActionEvent
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.vehicle_model import VehicleModel

logger = logging.getLogger("FlashPoint")


class DismountVehicleEvent(ActionEvent):

    def __init__(self,  vehicle_type:str, player: PlayerModel=None, player_index: int=None):
        super().__init__()
        self._game: GameStateModel = GameStateModel.instance()
        if player:
            self._player_index = self._game.players.index(player)
        elif player_index is not None:
            self._player_index = player_index

        self._vehicle_type = vehicle_type

    def execute(self, *args, **kwargs):
        print()
        logger.info("Executing DismountVehicleEvent")
        player = self._game.players[self._player_index]
        game_board: GameBoardModel = self._game.game_board
        vehicle: VehicleModel = game_board.ambulance if self._vehicle_type == "AMBULANCE" else game_board.engine
        vehicle.remove_passenger(player)
        logger.info(f"Player: {player.nickname} has dismounted the {self._vehicle_type}")
