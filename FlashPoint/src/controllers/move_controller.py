import src.constants.color as Color
from src.action_events.action_event import ActionEvent
from src.action_events.turn_events.move_event import MoveEvent
from src.constants.state_enums import DoorStatusEnum, WallStatusEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.scenes.game_board_scene import GameBoardScene
from src.sprites.game_board import GameBoard




class MoveController(object):

    def __init__(self, tile_destination: TileModel, game_board: GameBoard):
        super().__init__()
        self.board = game_board
        self.destination = tile_destination
        self.is_valid = False
        self.player = GameStateModel.instance().players_turn()
        self.directions = ["North", "West", "South", "East"]
        self.reachable_tiles = []
        self.valid = self.check_valid()
        if self.valid:
            MoveEvent()

    def update_reachable_tiles(self):
        for tile in self.reachable_tiles:
            x_pos = tile.x_coord
            y_pos = tile.y_coord
            assoc_tile_sprite = self.board.grid.grid[x_pos][y_pos]
            # Now make colour of those light up green on hover

            assoc_tile_sprite.hover_color = Color.GREEN

    def check_valid(self):
        num_ap = self.player.ap
        curr_location = GameStateModel.instance().game_board.get_tile_at(self.player.x_pos, self.player.y_pos)
        cost = 0
        cost = self.compute_distance(curr_location, cost, num_ap)
        if cost >= 0:
            return True
        else:
            return False

    def compute_distance(self, curr_location: TileModel, cost: int, num_ap: int):
        if curr_location == self.destination:
            return cost
        if num_ap == 0:
            return -1
        for d in self.directions:
            no_obstacle = False
            obstacle = curr_location.get_obstacle_in_direction(d)
            if isinstance(obstacle, WallModel):  # there might be a broken wall
                if obstacle.wall_status == WallStatusEnum.DESTROYED:
                    no_obstacle = True
            if isinstance(obstacle, DoorModel):  # there might be a destroyed or open door
                if obstacle.door_status == DoorStatusEnum.OPEN or obstacle.door_status == DoorStatusEnum.DESTROYED:
                    no_obstacle = True
            if obstacle is None:  # there might not be any obstacle
                no_obstacle = True

            if no_obstacle:
                next_tile = curr_location.get_tile_in_direction(d)
                self.reachable_tiles.append(next_tile)
                cost = self.compute_distance(next_tile, cost + 1, num_ap - 1)

    def update(self):
        for tile in self.board.grid.grid:  # First make them all hover_color to red
            tile.hover_color = Color.RED

        # Then, make the reachable ones to green
        for tiles in self.reachable_tiles:
            tiles.hover_color = Color.GREEN
