from src.controllers.command_player_controller import CommandPlayerController
from src.controllers.controller import Controller
from src.controllers.drive_vehicles_controller import DriveVehiclesController
from src.controllers.hazmat_controller import HazmatController
from src.controllers.identify_controller import IdentifyController
from src.controllers.vehicle_placement_controller import VehiclePlacementController
from src.controllers.victim_controller import VictimController
from src.core.event_queue import EventQueue
from src.models.game_board.tile_model import TileModel
from src.observers.game_state_observer import GameStateObserver
from src.sprites.tile_sprite import TileSprite
from src.sprites.game_board import GameBoard
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import GameStateEnum, GameKindEnum
from src.controllers.choose_starting_position_controller import ChooseStartingPositionController
from src.controllers.extinguish_controller import ExtinguishController
from src.controllers.move_controller import MoveController
from src.models.game_state_model import GameStateModel
from src.UIComponents.interactable import Interactable


class TileInputController(GameStateObserver, Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        if TileInputController._instance:
            raise Exception("TileInputController is a singleton")

        self.game_board_sprite = GameBoard.instance()

        ExtinguishController(current_player)
        MoveController(current_player)
        ChooseStartingPositionController(current_player)
        VictimController(current_player)

        if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
            VehiclePlacementController(current_player)
            DriveVehiclesController(current_player)
            IdentifyController(current_player)
            HazmatController(current_player)
            CommandPlayerController(current_player)

        GameStateModel.instance().add_observer(self)
        # Force notify observers
        GameStateModel.instance().state = GameStateModel.instance().state

        TileInputController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    @staticmethod
    def __del__():
        ExtinguishController._instance = None
        MoveController._instance = None
        ChooseStartingPositionController._instance = None
        TileInputController._instance = None
        VictimController._instance = None
        VehiclePlacementController._instance = None
        DriveVehiclesController._instance = None
        IdentifyController._instance = None
        HazmatController._instance = None
        CommandPlayerController._instance = None

    def _disable_all_menus(self):
        grid = self.game_board_sprite.grid.grid
        for column in range(len(grid)):
            for row in range(len(grid[column])):
                tile = grid[column][row]
                tile.disable_all()

    def run_checks(self, tile_model: TileModel):
        """Empty because this controller delegates to other controllers."""
        pass

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        """Empty because this controller delegates to other controllers."""
        pass

    def process_input(self, tile_sprite: TileSprite):
        self._disable_all_menus()
        MoveController.instance().process_input(tile_sprite)
        ExtinguishController.instance().process_input(tile_sprite)
        VictimController.instance().process_input(tile_sprite)

        if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
            IdentifyController.instance().process_input(tile_sprite)
            DriveVehiclesController.instance().process_input(tile_sprite)
            HazmatController.instance().process_input(tile_sprite)
            CommandPlayerController.instance().process_input(tile_sprite)

    def notify_player_index(self, player_index: int):
        pass

    def notify_game_state(self, state: GameStateEnum):
        on_click = None
        if state == GameStateEnum.PLACING_PLAYERS:
            on_click = ChooseStartingPositionController.instance().process_input

        elif state == GameStateEnum.PLACING_VEHICLES:
            VehiclePlacementController.instance().enable_prompts()
            on_click = VehiclePlacementController.instance().process_input

        elif state == GameStateEnum.MAIN_GAME:
            on_click = self.process_input

        grid = self.game_board_sprite.grid.grid
        for column in range(len(grid)):
            for row in range(len(grid[column])):
                tile = grid[column][row]
                tile.on_click(on_click, tile)

    def damage_changed(self, new_damage: int):
        pass

    def saved_victims(self, victims_saved: int):
        pass

    def dead_victims(self, victims_dead: int):
        pass

    def player_added(self, player: PlayerModel):
        pass

    def player_removed(self, player: PlayerModel):
        pass

    def player_command(self, source: PlayerModel, target: PlayerModel):
        pass

    @staticmethod
    def update(event_queue: EventQueue):
        MoveController.instance().update(event_queue)
        ChooseStartingPositionController.instance().update(event_queue)

        if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
            VehiclePlacementController.instance().update(event_queue)
