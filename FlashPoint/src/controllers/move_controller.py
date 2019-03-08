from typing import List

import src.constants.color as Color
from constants.state_enums import PlayerStatusEnum
from src.observers.player_observer import PlayerObserver
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.action_events.turn_events.move_event import MoveEvent
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.models.game_board.null_model import NullModel
from src.sprites.tile_sprite import TileSprite
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import DoorStatusEnum, WallStatusEnum, SpaceStatusEnum, GameStateEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard


class MoveController(PlayerObserver):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        if MoveController._instance:
            raise Exception("MoveController is a singleton")
        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.x_pos, self.current_player.y_pos, self.current_player.ap, [])
        self.current_player.add_observer(self)
        GameStateModel.instance().game_board.reset_tiles_visit_status()
        MoveController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def _determine_reachable_tiles(self, row: int, column: int, ap: int, movable_tiles: List[TileModel]) -> List[TileModel]:

        current_tile: TileModel = GameStateModel.instance().game_board.get_tile_at(row, column)
        current_tile.visit_count += 1
        if ap < 1:
            if current_tile.space_status == SpaceStatusEnum.FIRE:
                if current_tile in movable_tiles:
                    movable_tiles.remove(current_tile)
            return movable_tiles

        if ap < 3 and current_tile.space_status == SpaceStatusEnum.FIRE:
            open_tiles = []
            for direction, tile in current_tile.adjacent_tiles.items():
                obstacle = current_tile.adjacent_edge_objects[direction]
                if isinstance(obstacle, NullModel) or \
                   (isinstance(obstacle, DoorModel) and (obstacle.door_status == DoorStatusEnum.OPEN or obstacle.door_status == DoorStatusEnum.DESTROYED))\
                    or (isinstance(obstacle, WallModel) and obstacle.wall_status == WallStatusEnum.DESTROYED):
                        open_tiles.append(tile)

            if not [tile for tile in open_tiles if tile.space_status != SpaceStatusEnum.FIRE]:
                if current_tile in movable_tiles:
                    movable_tiles.remove(current_tile)
                    return movable_tiles

        for key in current_tile.adjacent_edge_objects.keys():
            tile: TileModel = current_tile.adjacent_tiles.get(key)
            obstacle: EdgeObstacleModel = current_tile.adjacent_edge_objects.get(key)
            if isinstance(tile, NullModel) or tile.visit_count > 3:
                continue

            ap_deduct = 2 if tile.space_status == SpaceStatusEnum.FIRE else 1

            if isinstance(obstacle, NullModel):

                movable_tiles.append(tile)
                movable_tiles += self._determine_reachable_tiles(tile.x_coord, tile.y_coord, ap - ap_deduct,
                                                                 movable_tiles)
            elif isinstance(obstacle, WallModel):
                if obstacle.wall_status == WallStatusEnum.DESTROYED:
                    movable_tiles.append(tile)
                    movable_tiles += self._determine_reachable_tiles(tile.x_coord, tile.y_coord, ap - ap_deduct,
                                                                     movable_tiles)
            elif isinstance(obstacle, DoorModel):
                if obstacle.door_status == DoorStatusEnum.OPEN or obstacle.door_status == DoorStatusEnum.DESTROYED:
                    movable_tiles.append(tile)
                    movable_tiles += self._determine_reachable_tiles(tile.x_coord, tile.y_coord, ap - ap_deduct,
                                                                     movable_tiles)
        # Remove duplicates
        output = list(set(movable_tiles))
        return output

    def _run_checks(self, tile_model: TileModel) -> bool:
        return tile_model in self.moveable_tiles

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self._run_checks(tile_model):
            return

        event = MoveEvent(tile_model)
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

    def update(self, event_queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return

        for column in range(len(self.game_board_sprite.grid.grid)):  # First make them all hover_color to red
            for row in range(len(self.game_board_sprite.grid.grid[column])):

                tile_model = GameStateModel.instance().game_board.get_tile_at(row, column)
                if self._run_checks(tile_model):
                    self.game_board_sprite.grid.grid[column][row].hover_color = Color.GREEN
                else:
                    self.game_board_sprite.grid.grid[column][row].hover_color = Color.RED

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def player_ap_changed(self, updated_ap: int):
        pass

    def player_special_ap_changed(self, updated_ap: int):
        pass

    def player_position_changed(self, x_pos: int, y_pos: int):

        GameStateModel.instance().game_board.reset_tiles_visit_status()
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.x_pos, self.current_player.y_pos, self.current_player.ap, [])
        GameStateModel.instance().game_board.reset_tiles_visit_status()

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass
