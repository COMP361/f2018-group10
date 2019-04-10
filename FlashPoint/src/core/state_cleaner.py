from src.controllers.veteran_controller import VeteranController
from src.controllers.chop_controller import ChopController
from src.controllers.door_controller import DoorController
from src.controllers.tile_input_controller import TileInputController
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard


class StateCleaner:
    @staticmethod
    def clear():
        # Reset everything
        if GameStateModel.instance():
            GameStateModel.destroy()
        if GameBoard.instance():
            GameBoard._instance = None
            # TileInputController.destroy()
            ChopController._instance = None
            DoorController._instance = None
            VeteranController._instance = None
