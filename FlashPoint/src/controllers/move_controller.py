from typing import List

import src.constants.color as Color
from src.constants.state_enums import PlayerStatusEnum

from src.models.game_units.victim_model import VictimModel
from src.observers.player_observer import PlayerObserver
from src.core.event_queue import EventQueue
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
            self.current_player.row, self.current_player.column, self.current_player.ap, [])
        self.current_player.add_observer(self)
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        MoveController._instance = self
        self.move_to = None
        self.is_moveable = False

    @classmethod
    def instance(cls):
        return cls._instance

    def _determine_reachable_tiles(self, row: int, column: int, ap: int, movable_tiles: List[TileModel]) -> List[TileModel]:

        current_tile: TileModel = GameStateModel.instance().game_board.get_tile_at(row, column)
        current_tile.visit_count += 1
        is_carrying_victim = False
        ap_multiplier = 1
        if isinstance(self.current_player.carrying_victim, VictimModel):
            is_carrying_victim = True
            ap_multiplier = 2
        else:
            is_carrying_victim = False

        # Base case where carrying victim and on fire.
        if is_carrying_victim and current_tile.space_status == SpaceStatusEnum.FIRE:
            if current_tile in movable_tiles:
                movable_tiles.remove(current_tile)
            return movable_tiles

        # Base case where you run out of AP
        if ap < 1:
            if current_tile.space_status == SpaceStatusEnum.FIRE:
                if current_tile in movable_tiles:
                    movable_tiles.remove(current_tile)
            return movable_tiles

        # Base case where you have less AP and are standing on fire, you cannot move to a place on fire.
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

        # Main recursive loop
        for key in current_tile.adjacent_edge_objects.keys():
            tile: TileModel = current_tile.adjacent_tiles.get(key)
            obstacle: EdgeObstacleModel = current_tile.adjacent_edge_objects.get(key)
            if isinstance(tile, NullModel) or tile.visit_count > 3:
                continue

            ap_deduct = 2 if tile.space_status == SpaceStatusEnum.FIRE else 1

            if isinstance(obstacle, NullModel):

                movable_tiles.append(tile)
                movable_tiles += self._determine_reachable_tiles(tile.row, tile.column, ap - ap_deduct*ap_multiplier,
                                                                 movable_tiles)
            elif isinstance(obstacle, WallModel):
                if obstacle.wall_status == WallStatusEnum.DESTROYED:
                    movable_tiles.append(tile)
                    movable_tiles += self._determine_reachable_tiles(tile.row, tile.column, ap - ap_deduct*ap_multiplier,
                                                                     movable_tiles)
            elif isinstance(obstacle, DoorModel):
                if obstacle.door_status == DoorStatusEnum.OPEN or obstacle.door_status == DoorStatusEnum.DESTROYED:
                    movable_tiles.append(tile)
                    movable_tiles += self._determine_reachable_tiles(tile.row, tile.column, ap - ap_deduct*ap_multiplier,
                                                                     movable_tiles)
        # Remove duplicates
        output = list(set(movable_tiles))
        return output

    def _run_checks(self, tile_model: TileModel) -> bool:
        if self.current_player != GameStateModel.instance().players_turn:
            return False
        return tile_model in self.moveable_tiles

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        # close the menu when other tile is clicked
        if self.move_to:
            self.move_to.disable_move()
            self.move_to.move_button.disable()
            self.move_to = None

        if not self._run_checks(tile_model):
            tile_sprite.disable_move()
            self.is_moveable = False
            return

        self.move_to = tile_sprite
        self.move_to.enable_move()
        self.move_to.move_button.enable()
        self.is_moveable = True

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
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, self.current_player.ap, [])
        GameStateModel.instance().game_board.reset_tiles_visit_count()

    def player_special_ap_changed(self, updated_ap: int):
        pass

    def player_position_changed(self, x_pos: int, y_pos: int):

        GameStateModel.instance().game_board.reset_tiles_visit_count()
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, self.current_player.ap, [])
        GameStateModel.instance().game_board.reset_tiles_visit_count()

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass
