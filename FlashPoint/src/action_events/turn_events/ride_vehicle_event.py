import logging

from src.action_events.action_event import ActionEvent
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.ambulance_model import AmbulanceModel
from src.models.game_units.engine_model import EngineModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.vehicle_model import VehicleModel

logger = logging.getLogger("FlashPoint")


class RideVehicleEvent(ActionEvent):
    """Add given player to the specified vehicle"""
    def __init__(self, vehicle_type: str, player: PlayerModel = None, player_index=None):
        super().__init__()
        if player:
            self._player_index = GameStateModel.instance().players.index(player)
        elif player_index is not None:
            self._player_index = player_index

        self._vehicle_type = vehicle_type

    def execute(self, *args, **kwargs):
        logger.info("Executing RideVehicleEvent")
        game_state: GameStateModel = GameStateModel.instance()
        game_board: GameBoardModel = game_state.game_board
        passenger = game_state.players[self._player_index]

        if self._vehicle_type == "AMBULANCE":
            game_board.ambulance.add_passenger(passenger)
        elif self._vehicle_type == "ENGINE":
            game_board.engine.add_passenger(passenger)

        logger.info(f"{passenger.nickname} is now a passenger of the {self._vehicle_type}")

