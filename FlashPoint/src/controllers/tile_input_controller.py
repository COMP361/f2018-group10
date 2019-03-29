from src.action_events.turn_events.drive_ambulance_event import DriveAmbulanceEvent
from src.controllers.identify_controller import IdentifyController
from src.controllers.vehicle_controller import VehicleController
from src.action_events.turn_events.drop_victim_event import DropVictimEvent
from src.action_events.turn_events.extinguish_event import ExtinguishEvent
from src.action_events.turn_events.move_event import MoveEvent
from src.action_events.turn_events.pick_up_victim_event import PickupVictimEvent
from src.controllers.victim_controller import VictimController
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.models.game_board.null_model import NullModel
from src.models.game_board.tile_model import TileModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.tile_sprite import TileSprite
from src.sprites.game_board import GameBoard
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import GameStateEnum, GameKindEnum
from src.controllers.choose_starting_position_controller import ChooseStartingPositionController
from src.controllers.extinguish_controller import ExtinguishController
from src.controllers.move_controller import MoveController
from src.models.game_state_model import GameStateModel
from src.observers.game_state_observer import GameStateObserver


class TileInputController(GameStateObserver):

    def damage_changed(self, new_damage: int):
        pass

    def saved_victims(self, victims_saved: int):
        pass

    def dead_victims(self, victims_dead: int):
        pass

    _instance = None

    def __init__(self, current_player: PlayerModel):
        if TileInputController._instance:
            raise Exception("TileInputController is a singleton")

        self.extinguish_controller = ExtinguishController(current_player)
        self.game_board_sprite = GameBoard.instance()
        self.move_controller = MoveController(current_player)
        self.choose_starting_controller = ChooseStartingPositionController(current_player)
        self.victim_controller = VictimController()

        if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
            self.vehicle_controller = VehicleController(current_player)
            self.identify_controller = IdentifyController(current_player)
        GameStateModel.instance().add_observer(self)
        self.fireman = current_player
        self.last_tile: TileSprite = None
        current_player.ap = 4
        GameStateModel.instance().state = GameStateEnum.PLACING_PLAYERS
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
        VehicleController._instance = None
        IdentifyController._instance = None


    def main_game_input(self, tile: TileSprite):
        self.move_controller.process_input(tile)
        self.extinguish_controller.process_input(tile)
        self.victim_controller.process_input(tile)
        if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
            self.vehicle_controller.process_input_main_game(tile)

        tile_model = GameStateModel.instance().game_board.get_tile_at(tile.row, tile.column)
        if tile.menu_shown:
            if self.move_controller.is_moveable:
                self.move_controller.move_to.move_button.on_click(self.execute_move_event, tile_model)

            if self.extinguish_controller.extinguishable:
                self.extinguish_controller.fire_tile.extinguish_button.on_click(self.execute_extinguish_event, tile_model)

            if self.victim_controller.can_drop:
                victim: VictimModel = self.fireman.carrying_victim
                if not isinstance(victim, NullModel):
                    self.victim_controller.action_tile.drop_victim_button.on_click(self.execute_drop_event, victim)

            elif self.victim_controller.can_pickup:
                victim: VictimModel = None
                board = GameStateModel.instance().game_board
                for assoc_model in board.get_tile_at(tile.row, tile.column).associated_models:
                    if isinstance(assoc_model, VictimModel):
                            victim = assoc_model

                if victim:
                    self.victim_controller.action_tile.pickup_victim_button.on_click(self.execute_pickup_event, victim)

            if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
                tile.drive_ambulance_here_button.on_click(self.execute_drive_ambulance_event, tile_model)

        if not tile.menu_shown:
            tile.menu_shown = True
            if self.last_tile:
                self.last_tile.menu_shown = False
            self.last_tile = tile

    def place_vehicles(self, tile_sprite: TileSprite):
        self.vehicle_controller.process_input_placement(tile_sprite)

    def execute_drive_ambulance_event(self, tile_model: TileModel):
        if not self.vehicle_controller._run_drive_checks(tile_model):
            return
        
        second_tile = GameStateModel.instance().game_board.get_other_parking_tile(tile_model)
        event = DriveAmbulanceEvent((tile_model, second_tile))
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def execute_drop_event(self, victim: VictimModel):
        event = DropVictimEvent(victim)
        self.victim_controller.process_input(GameBoard.instance().grid.grid[victim.column][victim.row])
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def execute_pickup_event(self, victim: VictimModel):
        event = PickupVictimEvent(victim)
        self.victim_controller.process_input(GameBoard.instance().grid.grid[victim.column][victim.row])
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def execute_extinguish_event(self, tile: TileModel):
        if not self.extinguish_controller._run_checks(tile):
            return

        event = ExtinguishEvent(tile)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

    def execute_move_event(self, tile: TileModel):
        self.move_controller.move_to.disable_move()
        event = MoveEvent(tile, self.move_controller.moveable_tiles)
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

    def notify_player_index(self, player_index: int):
        pass

    def notify_game_state(self, state: GameStateEnum):
        on_click = None
        if state == GameStateEnum.PLACING_PLAYERS:
            on_click = self.choose_starting_controller.process_input
        elif state == GameStateEnum.PLACING_VEHICLES:
            self.vehicle_controller.enable_prompts()
            on_click = self.vehicle_controller.process_input_placement
        elif state == GameStateEnum.MAIN_GAME:
            on_click = self.main_game_input

        grid = self.game_board_sprite.grid.grid
        for column in range(len(grid)):
            for row in range(len(grid[column])):
                tile = grid[column][row]
                tile.on_click(on_click, tile)

    def update(self, event_queue: EventQueue):
        self.move_controller.update(event_queue)
        self.choose_starting_controller.update(event_queue)
        self.extinguish_controller.update(event_queue)
        self.victim_controller.update(event_queue)
        if GameStateModel.instance().rules == GameKindEnum.EXPERIENCED:
            self.vehicle_controller.update(event_queue)
