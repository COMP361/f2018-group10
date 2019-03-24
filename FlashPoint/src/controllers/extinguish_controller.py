from src.core.event_queue import EventQueue
from src.models.game_board.door_model import DoorModel
from src.models.game_board.wall_model import WallModel
from src.sprites.tile_sprite import TileSprite
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import SpaceStatusEnum, GameStateEnum, WallStatusEnum, DoorStatusEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard


class ExtinguishController(object):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        if ExtinguishController._instance:
            raise Exception("ExtinguishController is a singleton")
        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        game: GameStateModel = GameStateModel.instance()
        game.game_board.reset_tiles_visit_count()
        ExtinguishController._instance = self
        self.extinguishable = False
        self.fire_tile = None  # this is the previously opened menu for extinguish

    @classmethod
    def instance(cls):
        return cls._instance

    def _run_checks(self, tile_model: TileModel) -> bool:
        player_tile: TileModel = GameStateModel.instance().game_board.get_tile_at(self.current_player.row,
                                                                                  self.current_player.column)

        valid_to_extinguish = tile_model == player_tile or tile_model == player_tile.north_tile \
                              or tile_model == player_tile.east_tile or tile_model == player_tile.west_tile \
                              or tile_model == player_tile.south_tile

        if not valid_to_extinguish:
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

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if self.fire_tile:
            self.fire_tile.disable_extinguish()
            self.fire_tile = None

        if not self._run_checks(tile_model):
            tile_sprite.disable_extinguish()
            self.extinguishable = False
            return

        self.extinguishable = True
        tile_sprite.enable_extinguish()
        self.fire_tile = tile_sprite

    def update(self, event_queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return
