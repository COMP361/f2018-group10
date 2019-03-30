from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.extinguish_event import ExtinguishEvent
from src.controllers.controller import Controller
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.models.game_board.door_model import DoorModel
from src.models.game_board.wall_model import WallModel
from src.sprites.tile_sprite import TileSprite
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import SpaceStatusEnum, GameStateEnum, WallStatusEnum, DoorStatusEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard


class ExtinguishController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if ExtinguishController._instance:
            raise Exception("ExtinguishController is a singleton")
        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        game: GameStateModel = GameStateModel.instance()
        game.game_board.reset_tiles_visit_count()

        ExtinguishController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def run_checks(self, tile_model: TileModel) -> bool:
        player_tile: TileModel = GameStateModel.instance().game_board.get_tile_at(self.current_player.row,
                                                                                  self.current_player.column)

        if player_tile not in player_tile.adjacent_tiles.values():
            return False

        if self.current_player.ap < 1:
            return False

        if tile_model.space_status == SpaceStatusEnum.SAFE:
            return False

        if player_tile.south_tile == tile_model:
            obs = player_tile.get_obstacle_in_direction('South')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        elif player_tile.north_tile == tile_model:
            obs = player_tile.get_obstacle_in_direction('North')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        elif player_tile.east_tile == tile_model:
            obs = player_tile.get_obstacle_in_direction('East')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        elif player_tile.west_tile == tile_model:
            obs = player_tile.get_obstacle_in_direction('West')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        return True

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.run_checks(tile_model):
            menu_to_close.disable()
            return

        event = ExtinguishEvent(tile_model)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

        menu_to_close.disable()

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self.run_checks(tile_model):
            tile_sprite.extinguish_button.disable()
            return

        tile_sprite.extinguish_button.enable()
        tile_sprite.extinguish_button.on_click(tile_sprite.extinguish_button)
