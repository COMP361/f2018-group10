from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.dismount_vehicle_event import DismountVehicleEvent
from src.action_events.turn_events.drive_vehicle_event import DriveVehicleEvent
from src.action_events.turn_events.ride_vehicle_event import RideVehicleEvent
from src.constants.state_enums import SpaceKindEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.tile_sprite import TileSprite


class DriveVehiclesController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        if DriveVehiclesController._instance:
            self._current_player = current_player
            # raise Exception(f"{DriveVehiclesController.__name__} is a singleton!")
        DriveVehiclesController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def _player_has_enough_ap(self, vehicle_type: str, tile_model: TileModel) -> bool:
        game_board: GameBoardModel = GameStateModel.instance().game_board
        destination_second_tile = game_board.get_other_parking_tile(tile_model)

        ap_multiplier = game_board.get_distance_to_parking_spot(vehicle_type, (tile_model, destination_second_tile))
        return self._current_player.ap >= 2 * ap_multiplier

    def _player_is_in_vehicle_space(self, vehicle_type: str, first_tile: TileModel) -> bool:
        game_board: GameBoardModel = GameStateModel.instance().game_board
        player = self._current_player

        space_kind = SpaceKindEnum.AMBULANCE_PARKING if vehicle_type == "AMBULANCE" else SpaceKindEnum.ENGINE_PARKING
        if first_tile.space_kind != space_kind:
            return False

        second_tile = game_board.get_other_parking_tile(first_tile)

        vehicle = game_board.ambulance if vehicle_type == "AMBULANCE" else game_board.engine
        vehicle_row = vehicle.row
        vehicle_column = vehicle.column
        row_match = player.row == first_tile.row or player.row == second_tile.row
        column_match = player.column == first_tile.column or player.row == second_tile.column
        if not row_match or not column_match:
            return False

        row_match = player.row == vehicle_row or player.row == vehicle_row + 1
        column_match = player.column == vehicle_column or player.column == vehicle_column + 1
        return row_match and column_match

    def _run_checks_drive_ambulance(self, tile_model: TileModel):
        # Doge cannot drive ambulance
        if self._current_player.role == PlayerRoleEnum.DOGE:
            return False

        if self._current_player != GameStateModel.instance().players_turn:
            return False

        if tile_model.space_kind != SpaceKindEnum.AMBULANCE_PARKING:
            return False

        if not self._player_has_enough_ap("AMBULANCE", tile_model):
            return False
        return True

    def _run_checks_drive_engine(self, tile_model: TileModel) -> bool:
        # Doge cannot drive engine
        if self._current_player.role == PlayerRoleEnum.DOGE:
            return False

        if self._current_player != GameStateModel.instance().players_turn:
            return False

        if tile_model.space_kind != SpaceKindEnum.ENGINE_PARKING:
            return False

        if self._current_player not in GameStateModel.instance().game_board.engine.passengers:
            return False

        if not self._player_has_enough_ap("ENGINE", tile_model):
            return False

        return True

    def _run_checks_ride_vehicle(self, tile_model: TileModel, vehicle_type: str):
        # Doge cannot ride vehicle
        if self._current_player.role == PlayerRoleEnum.DOGE:
            return False

        ambulance = GameStateModel.instance().game_board.ambulance
        engine = GameStateModel.instance().game_board.engine

        player_is_riding = self._current_player in ambulance.passengers or self._current_player in engine.passengers
        return self._player_is_in_vehicle_space(vehicle_type, tile_model) and not player_is_riding

    def _run_checks_dismount_vehicle(self, tile_model: TileModel, vehicle_type: str):
        # Doge cannot dismount vehicle
        if self._current_player.role == PlayerRoleEnum.DOGE:
            return False

        game_board: GameBoardModel = GameStateModel.instance().game_board
        vehicle = game_board.ambulance if vehicle_type == "AMBULANCE" else game_board.engine
        player_is_riding = self._current_player in vehicle.passengers

        return self._player_is_in_vehicle_space(vehicle_type, tile_model) and player_is_riding

    def run_checks(self, tile_model: TileModel) -> bool:
        """Not used since this controller has many different checks"""
        pass

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        parking_type = tile_model.space_kind
        vehicle_type = "AMBULANCE" if parking_type == SpaceKindEnum.AMBULANCE_PARKING else "ENGINE"

        event = None
        if self._run_checks_dismount_vehicle(tile_model, vehicle_type):
            event = DismountVehicleEvent(vehicle_type, player=self._current_player)
        elif self._run_checks_ride_vehicle(tile_model, vehicle_type):
            event = RideVehicleEvent(vehicle_type, player=self._current_player)
        elif self._run_checks_drive_ambulance(tile_model):
            second_tile = GameStateModel.instance().game_board.get_other_parking_tile(tile_model)
            event = DriveVehicleEvent("AMBULANCE", (tile_model, second_tile))
        elif self._run_checks_drive_engine(tile_model):
            second_tile = GameStateModel.instance().game_board.get_other_parking_tile(tile_model)
            event = DriveVehicleEvent("ENGINE", (tile_model, second_tile))
        else:
            menu_to_close.disable()
            return

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        menu_to_close.disable()

    def process_input(self, tile_sprite: TileSprite):
        game_state: GameStateModel = GameStateModel.instance()
        tile_model = game_state.game_board.get_tile_at(tile_sprite.row, tile_sprite.column)
        parking_type = tile_model.space_kind
        vehicle_type = "AMBULANCE" if parking_type == SpaceKindEnum.AMBULANCE_PARKING else "ENGINE"

        button = None

        if self._run_checks_dismount_vehicle(tile_model, vehicle_type):
            button = tile_sprite.dismount_vehicle_button
            tile_sprite.ride_vehicle_button.disable()

        elif self._run_checks_ride_vehicle(tile_model, vehicle_type):
            button = tile_sprite.ride_vehicle_button
            tile_sprite.dismount_vehicle_button.disable()

        elif self._run_checks_drive_ambulance(tile_model):
            button = tile_sprite.drive_ambulance_here_button
            tile_sprite.drive_engine_here_button.disable()

        elif self._run_checks_drive_engine(tile_model):
            button = tile_sprite.drive_engine_here_button
            tile_sprite.drive_ambulance_here_button.disable()

        if button:
            button.enable()
            button.on_click(self.send_event_and_close_menu, tile_model, button)
        else:
            tile_sprite.drive_ambulance_here_button.disable()
            tile_sprite.drive_engine_here_button.disable()
            tile_sprite.dismount_vehicle_button.disable()
            tile_sprite.ride_vehicle_button.disable()
