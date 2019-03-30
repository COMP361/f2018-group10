from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import GameKindEnum, WallStatusEnum, DoorStatusEnum, SpaceStatusEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.sprites.tile_sprite import TileSprite


class HazmatController(object):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board
        self.current_player = current_player
        if HazmatController._instance:
            raise Exception("HazmatController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("HazmatController should not exist in Family Mode!")

    @classmethod
    def instance(cls):
        return cls._instance

    def check(self, tile_model: TileModel) -> bool:
        player_tile: TileModel = GameStateModel.instance().game_board.get_tile_at(self.current_player.row,
                                                                                  self.current_player.column)

        if not self.current_player == self.game.players_turn:
            return False

        valid_to_identify = TurnEvent.has_required_AP(self.current_player.ap, 2)
        if not valid_to_identify:
            return False

        valid_to_extinguish = tile_model == player_tile or tile_model == player_tile.north_tile \
                              or tile_model == player_tile.east_tile or tile_model == player_tile.west_tile \
                              or tile_model == player_tile.south_tile

        if not valid_to_extinguish:
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

        for model in tile_model.associated_models:
            if isinstance(model, HazmatModel):
                return True

        return False

    def process_input(self, tile_sprite: TileSprite):
        tile = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)
        if self.check(tile):
            tile_sprite.hazmat_button.enable()
        else:
            tile_sprite.hazmat_button.disable()
