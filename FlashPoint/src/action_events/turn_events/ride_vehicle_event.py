from src.action_events.action_event import ActionEvent
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.ambulance_model import AmbulanceModel
from src.models.game_units.engine_model import EngineModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.vehicle_model import VehicleModel


class RideVehicleEvent(ActionEvent):
    """Add given player to the specified vehicle"""
    def __init__(self, player: PlayerModel, vehicle: VehicleModel):
        super().__init__()
        self._player_index = GameStateModel.instance().players.index(player)

        if isinstance(vehicle, AmbulanceModel):
            self._vehicle_type = "AMBULANCE"
        elif isinstance(vehicle, EngineModel):
            self._vehicle_type = "ENGINE"
        else:
            raise Exception(f"Unrecognized type: {vehicle.__class__} was passed as a vehicle.")

    def execute(self, *args, **kwargs):
        game_state: GameStateModel = GameStateModel.instance()
        game_board: GameBoardModel = game_state.game_board
        passenger = game_state.players[self._player_index]

        if self._vehicle_type == "AMBULANCE":
            game_board.ambulance.add_passenger(passenger)
        elif self._vehicle_type == "ENGINE":
            game_board.engine.add_passenger(passenger)
