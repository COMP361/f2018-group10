from src.action_events.action_event import ActionEvent
from src.action_events.turn_events.knock_down_event import KnockDownEvent
from src.constants.state_enums import WallStatusEnum, SpaceStatusEnum, SpaceKindEnum, VictimStateEnum, DoorStatusEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class AdvanceFireEvent(ActionEvent):

    def __init__(self):
        super().__init__()
        self.game_state: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game_state.game_board
        self.initial_tile: TileModel = None
        self._red_dice = None
        self._black_dice = None

    def execute(self, *args, **kwargs):
        # Pick random location
        if not self._red_dice:
            # roll dice
            self._red_dice = self.game_state.roll_red_dice
        if not self._black_dice:
            self._black_dice = self.game_state.roll_black_dice
        # next step is to determine what that tile contains.
        self.set_tile()
        self.check_associated_models(self.initial_tile)
        status = self.initial_tile.space_status()
        if status is SpaceStatusEnum.SAFE or status is SpaceStatusEnum.SMOKE:
            self.initial_tile.space_status = SpaceStatusEnum.FIRE

        elif status is SpaceStatusEnum.FIRE:
            self.explosion()

        self.flash_over()

    def set_tile(self):
        self.initial_tile = self.board.get_tile_at(self._red_dice,
                                                   self._black_dice)  # gets starting tile of advance fire.

    def check_associated_models(self, tile: TileModel):
        assoc_models = tile.associated_models()
        for model in assoc_models:
            if isinstance(model, PlayerModel):
                KnockDownEvent(model).execute()

            elif isinstance(model, VictimModel):
                self.game_state.victims_lost = self.game_state.victims_lost + 1
                model: VictimModel = model
                model.state = VictimStateEnum.LOST

            elif isinstance(model, POIModel):
                model: POIModel = model
                model.reveal()

            else:
                pass

    def explosion(self):
        # fire has to go in all 4 directions:
        # NORTH, WEST, SOUTH, EAST
        list_directions = ["North", "West", "South", "East"]
        for d in list_directions:
            self.advance(d, self.initial_tile)

    def flash_over(self):
        directions = ["North", "West", "South", "East"]
        all_tiles = self.board.get_tiles()
        for tile in all_tiles:  # go through all tiles of the board
            if tile.space_kind is SpaceKindEnum.INDOOR:  # check if it is indoors
                if tile.space_status is SpaceStatusEnum.SMOKE:
                    for d in directions:  # loop in all directions
                        adj_tile = tile.get_tile_in_direction(d)  # get adjacent tile
                        if adj_tile.space_status() is SpaceStatusEnum.FIRE:  # if adacent tile is fire, place this
                            # tile's smoke status to fire status.
                            tile.space_status = SpaceStatusEnum.FIRE  # set to fire
                            break  # break or else we are looping for nothing

    def advance(self, d: str, tile: TileModel):
        self.check_associated_models(tile)

        obstacle = self.initial_tile.get_obstacle_in_direction(d)
        if isinstance(obstacle, WallModel):
            status = obstacle.wall_status()
            if status is WallStatusEnum.INTACT:  # checks whether wall is intact
                obstacle.damage_wall()  # make it damaged.
                damage = self.game_state.damage
                self.game_state.damage = damage + 1  # increment damage count.

            elif status is WallStatusEnum.DAMAGED:  # checks if wall is damaged
                obstacle.destroy_wall()
                damage = self.game_state.damage
                self.game_state.damage = damage + 1  # increment damage count

            elif status is WallStatusEnum.DESTROYED:
                next_tile: TileModel = tile.get_tile_in_direction(d)
                if next_tile.space_kind is SpaceKindEnum.INDOOR:
                    if next_tile.space_status.FIRE:
                        self.advance(d, next_tile)

                    else:
                        next_tile.space_status = SpaceStatusEnum.FIRE

            # have to call advance

            elif isinstance(obstacle, DoorModel):
                if obstacle.door_status is DoorStatusEnum.CLOSED:
                    obstacle.destroy_door()

                elif obstacle.door_status is DoorStatusEnum.OPEN or obstacle.door_status is DoorStatusEnum.DESTROYED:
                    next_tile: TileModel = tile.get_tile_in_direction(d)
                    if next_tile.space_kind.INDOOR:
                        if next_tile.space_status.FIRE:
                            self.advance(d, next_tile)

                        else:
                            next_tile.space_status = SpaceStatusEnum.FIRE
