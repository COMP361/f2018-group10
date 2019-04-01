from typing import Tuple
import logging

from src.sprites.engine_sprite import EngineSprite
from src.sprites.game_board import GameBoard
from src.sprites.ambulance_sprite import AmbulanceSprite
from src.models.game_units.ambulance_model import AmbulanceModel
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.vehicle_model import VehicleModel
from src.models.game_board.tile_model import TileModel
from src.action_events.action_event import ActionEvent


logger = logging.getLogger("FlashPoint")


class VehiclePlacedEvent(ActionEvent):
    """Determining the parking spot will be up to the GUI. This will create required associations, set positions
       and set up observers."""

    def __init__(self, vehicle: VehicleModel = None, parking_spot: Tuple[TileModel] = None):
        super().__init__()
        self._vehicle_type = "AMBULANCE" if isinstance(vehicle, AmbulanceModel) else "ENGINE"

        self._row = min(tile.row for tile in parking_spot) if parking_spot else -1
        self._column = min(tile.column for tile in parking_spot) if parking_spot else -1

    def execute(self, *args, **kwargs):
        print()
        logger.info(f"Executing VehiclePlacedEvent: {self._vehicle_type} placed.")

        board_model: GameBoardModel = GameStateModel.instance().game_board
        board_sprite: GameBoard = GameBoard.instance()
        tile_sprite = board_sprite.grid.grid[self._column][self._row]
        if self._vehicle_type == "AMBULANCE":
            # Set ambulance position
            board_model.ambulance.drive((self._row, self._column))

            # Create AmbulanceSprite
            ambulance_sprite = AmbulanceSprite(board_model.ambulance.orientation, tile_sprite)
            board_model.ambulance.add_observer(ambulance_sprite)
            # Add to gameboard sprite group
            board_sprite.add(ambulance_sprite)

        else:
            # Set engine position
            board_model.engine.drive((self._row, self._column))

            # Create EngineSprite
            engine_sprite = EngineSprite(board_model.engine.orientation, tile_sprite)
            board_model.engine.add_observer(engine_sprite)
            # Add to gameboard sprite group
            board_sprite.add(engine_sprite)
