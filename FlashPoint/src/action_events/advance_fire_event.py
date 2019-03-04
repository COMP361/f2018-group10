from src.action_events.action_event import ActionEvent
from src.action_events.turn_events.knock_down_event import KnockDownEvent
from src.constants.state_enums import WallStatusEnum, SpaceStatusEnum, SpaceKindEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units import player_model
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class AdvanceFireEvent(ActionEvent):

    def __init__(self):
        super().__init__()
        self.game_state = GameStateModel.instance()
        self.board = self.game_state.gameboard()
        self.initial_tile = None
        self._red_dice = None
        self._black_dice = None

    def execute(self, *args, **kwargs):
        # Pick random location
        if not self._red_dice:
            # roll dice
            self._red_dice = self.game_state.roll_red_dice()
        if not self._black_dice:
            self._black_dice = self.game_state.roll_black_dice()
        # next step is to determine what that tile contains.
        self.get_tile()
        self.check_associated_models()
        status = self.initial_tile.space_status()
        if status is SpaceStatusEnum.SAFE or status is SpaceStatusEnum.SMOKE:
            self.initial_tile.set_status(SpaceStatusEnum.FIRE)

        elif status is SpaceStatusEnum.FIRE:
            self.explosion()

    def get_tile(self):
        self.initial_tile = self.board.get_tile_at(self._red_dice,
                                                   self._black_dice)  # gets starting tile of advance fire.

    def check_associated_models(self):
        assoc_models = self.initial_tile.associated_models()
        for model in assoc_models:
            if isinstance(player_model, model):
                KnockDownEvent(model).execute()
            if isinstance(VictimModel, model):
                victim_lost = self.game_state.victims_lost()
                self.game_state.victims_lost = victim_lost + 1
                model.set_dead()

            if isinstance(POIModel, model):
                model.reveal()

    def explosion(self):
        # fire has to go in all 4 directions:
        # NORTH, WEST, SOUTH, EAST
        list_directions = ["North", "West", "South", "East"]
        for d in list_directions:
            self.advance(d, self.initial_tile)

    def flash_over(self):
        pass

    def advance(self, d: str, tile: TileModel):

        if tile.space_status is not SpaceStatusEnum.FIRE:  # makes sure the advancement of fire is done throughout
            pass

        else:
            obstacle = self.initial_tile.get_obstacle_in_direction(d)
            if isinstance(WallModel, obstacle):
                status = obstacle.wall_status()
                if status is WallStatusEnum.INTACT:  # checks whether wall is intact
                    obstacle.damage_wall()  # make it damaged.
                    damage = self.game_state.damage()
                    self.game_state.damage = damage + 1  # increment damage count.

                elif status is WallStatusEnum.DAMAGED:  # checks if wall is damaged
                    obstacle.destroy_wall()
                    damage = self.game_state.damage()
                    self.game_state.damage = damage + 1  # increment damage count

                elif status is WallStatusEnum.DESTROYED:
                    next_tile: TileModel = tile.get_tile_in_direction(d)
                    if next_tile.space_kind is SpaceKindEnum.INDOOR:
                        if next_tile.space_status.FIRE:
                            self.advance(d, next_tile)

                        else:
                            next_tile.space_status = SpaceStatusEnum.FIRE

            # have to call advance

            elif isinstance(DoorModel, obstacle):
                if obstacle.DoorStatusEnum.CLOSED:
                    obstacle.destroy_door()

                elif obstacle.DoorStatusEnum.OPEN or obstacle.DoorStatusEnum.DESTROYED:
                    next_tile: TileModel = tile.get_tile_in_direction(d)
                    if next_tile.space_kind.INDOOR:
                        if next_tile.space_status.FIRE:
                            self.advance(d, next_tile)

                        else:
                            next_tile.space_status = SpaceStatusEnum.FIRE
