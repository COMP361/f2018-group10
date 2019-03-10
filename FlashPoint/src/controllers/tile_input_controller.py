from src.action_events.turn_events.move_event import MoveEvent
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.models.game_board.tile_model import TileModel
from src.sprites.tile_sprite import TileSprite
from src.sprites.game_board import GameBoard
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import GameStateEnum
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
        GameStateModel.instance().add_observer(self)
        current_player.ap = 4
        GameStateModel.instance().state = GameStateEnum.PLACING
        TileInputController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def move_and_extinguish(self, tile: TileSprite):
        self.move_controller.process_input(tile)
        self.extinguish_controller.process_input(tile)
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile.row, tile.column)
        if self.move_controller.is_moveable:
            self.move_controller.move_to.move_button.on_click(self.execute_move_event, tile_model)

    def execute_move_event(self, tile: TileModel):
        print("move_event created")
        self.move_controller.move_to.disable_move()
        event = MoveEvent(tile, self.move_controller.moveable_tiles)
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def notify_player_index(self, player_index: int):
        pass

    def notify_game_state(self, state: GameStateEnum):
        on_click = None
        if state == GameStateEnum.PLACING:
            on_click = self.choose_starting_controller.process_input
        elif state == GameStateEnum.MAIN_GAME:
            on_click = self.move_and_extinguish

        grid = self.game_board_sprite.grid.grid
        for column in range(len(grid)):
            for row in range(len(grid[column])):
                tile = grid[column][row]
                tile.on_click(on_click, tile)

    def update(self, event_queue: EventQueue):
        self.move_controller.update(event_queue)
        self.choose_starting_controller.update(event_queue)
