from src.action_events.action_event import ActionEvent
from src.action_events.turn_events.knock_down_event import KnockDownEvent
from src.constants.state_enums import WallStatusEnum, SpaceStatusEnum, SpaceKindEnum, VictimStateEnum, DoorStatusEnum, \
    POIStatusEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.null_model import NullModel
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
        self.red_dice = None
        self.black_dice = None
        self.directions = ["North", "South", "East", "West"]

    def execute(self, *args, **kwargs):
        # Pick random location: roll dice
        if not self.red_dice:
            self.red_dice = self.game_state.roll_red_dice()
        if not self.black_dice:
            self.black_dice = self.game_state.roll_black_dice()

        # Change state of tile depending on previous state
        self.initial_tile = self.board.get_tile_at(self.red_dice, self.black_dice)
        self.advance_on_tile(self.initial_tile)
        # TODO: reset every tile's visit status
        self.flashover()
        self.affect_damages()


    def advance_on_tile(self, target_tile: TileModel):
        target_tile.visited = True
        tile_status = target_tile.space_status
        # Safe -> Smoke
        if tile_status == SpaceStatusEnum.SAFE:
            target_tile.space_status = SpaceStatusEnum.SMOKE

        # Smoke -> Fire
        elif tile_status == SpaceStatusEnum.SMOKE:
            target_tile.space_status = SpaceStatusEnum.FIRE

        # Fire -> Explosion
        else:
            self.explosion(target_tile)


    def explosion(self, origin_tile: TileModel):
        for direction, obstacle in origin_tile.adjacent_edge_objects.items():
            # fire does not move to the neighbouring tile
            # damaging wall present along the tile
            if isinstance(obstacle, WallModel) and obstacle.wall_status != WallStatusEnum.DESTROYED:
                obstacle.inflict_damage()
                self.game_state.damage += 1

            # fire does not move to the neighbouring tile
            # removing door that borders the tile
            elif isinstance(obstacle, DoorModel):
                obstacle.destroy_door()

            # fire can move to the neighbouring tile
            # if the neighbouring tile is on fire, a shockwave is created
            # else it is just set on fire.
            else:
                nb_tile = origin_tile.get_tile_in_direction(direction)
                if nb_tile:
                    if nb_tile.space_status == SpaceStatusEnum.FIRE:
                        self.shockwave(nb_tile, direction)
                    else:
                        nb_tile.space_status = SpaceStatusEnum.FIRE



    def shockwave(self, tile: TileModel, direction: str):
        """
        Send shockwave along a direction.

        :param tile: the tile where the shockwave starts
        :param direction: direction in which shockwave continues
        :return:
        """
        should_stop = False
        while not should_stop:
            # if there is no obstacle in the given direction -
            #   if neighbouring tile is not on fire, set it to fire
            #   and stop the shockwave.
            #   else set the current tile to the neighbouring tile
            #   and continue the shockwave.
            if not tile.has_obstacle_in_direction(direction):
                nb_tile: TileModel = tile.get_tile_in_direction(direction)
                if nb_tile.space_status != SpaceStatusEnum.FIRE:
                    nb_tile.space_status = SpaceStatusEnum.FIRE
                    should_stop = True

                else:
                    tile = nb_tile

            # if there is an obstacle in the given direction,
            # shockwave should stop.
            else:
                # 1. if obstacle is a wall, inflict damage on it and increment
                #   game state damage.
                # 2. if obstacle is a non-destroyed door, destroy it.
                obstacle = tile.get_obstacle_in_direction(direction)
                if isinstance(obstacle, WallModel):
                    obstacle.inflict_damage()
                    self.game_state.damage += 1

                elif isinstance(obstacle, DoorModel) and obstacle.door_status != DoorStatusEnum.DESTROYED:
                    obstacle.destroy_door()

                else:
                    pass

                should_stop = True


    def flashover(self):
        """
        Convert all smokes adjacent to fires
        to smokes.
        """
        all_smokes_converted = False
        while not all_smokes_converted:
            num_converted = 0
            for tile in self.board.tiles:
                # if the tile does not have smoke,
                # skip this iteration
                if tile.space_status != SpaceStatusEnum.SMOKE:
                    continue

                # tile has smoke:
                # check if neighbour is not blocked by obstacle
                # and neighbour is not null. if neighbour on fire,
                # set current tile to fire.
                for direction, nb_tile in tile.adjacent_tiles.items():
                    if isinstance(nb_tile, NullModel):
                        continue

                    obstacle = tile.get_obstacle_in_direction(direction)
                    if isinstance(obstacle, WallModel) and obstacle.wall_status != WallStatusEnum.DESTROYED:
                        continue
                    elif isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.CLOSED:
                        continue
                    else:
                        pass

                    if nb_tile.space_status == SpaceStatusEnum.FIRE:
                        tile.space_status = SpaceStatusEnum.FIRE
                        num_converted += 1
                        break

            if num_converted == 0:
                all_smokes_converted = True


    def affect_damages(self):
        """
        Affect any valid damages to firemen,
        victims, POIs
        """
        for tile in self.board.tiles:
            assoc_models = tile.associated_models
            tile_status = tile.space_status
            if tile_status != SpaceStatusEnum.FIRE:
                continue

            for model in assoc_models:
                if isinstance(model, PlayerModel):
                    KnockDownEvent(model).execute()

                elif isinstance(model, VictimModel):
                    self.game_state.victims_lost += 1
                    model: VictimModel = model
                    model.state = VictimStateEnum.LOST

                elif isinstance(model, POIModel):
                    model.reveal()
                    model.status = POIStatusEnum.LOST

                else:
                    pass

        # removing any fire markers that were
        # placed outside of the building
        for tile in self.board.tiles:
            if tile.space_kind == SpaceKindEnum.OUTDOOR and tile.space_status == SpaceStatusEnum.FIRE:
                tile.space_status = SpaceStatusEnum.SAFE


    def check_associated_models(self, tile: TileModel):
        assoc_models = tile.associated_models()
        for model in assoc_models:
            if isinstance(model, PlayerModel):
                KnockDownEvent(model).execute()

            elif isinstance(model, VictimModel):
                self.game_state.victims_lost += 1
                model: VictimModel = model
                model.state = VictimStateEnum.LOST

            elif isinstance(model, POIModel):
                model: POIModel = model
                model.reveal()

            else:
                pass

    # def explosion(self):
    #     # fire has to go in all 4 directions:
    #     # NORTH, WEST, SOUTH, EAST
    #     list_directions = ["North", "West", "South", "East"]
    #     for d in list_directions:
    #         self.advance(d, self.initial_tile)

    # def flash_over(self):
    #     directions = ["North", "West", "South", "East"]
    #     all_tiles = self.board.get_tiles()
    #     for tile in all_tiles:  # go through all tiles of the board
    #         if tile.space_kind is SpaceKindEnum.INDOOR:  # check if it is indoors
    #             if tile.space_status is SpaceStatusEnum.SMOKE:
    #                 for d in directions:  # loop in all directions
    #                     adj_tile = tile.get_tile_in_direction(d)  # get adjacent tile
    #                     if adj_tile.space_status() is SpaceStatusEnum.FIRE:  # if adacent tile is fire, place this
    #                         # tile's smoke status to fire status.
    #                         tile.space_status = SpaceStatusEnum.FIRE  # set to fire
    #                         break  # break or else we are looping for nothing

    def advance(self, d: str, tile: TileModel):
        self.check_associated_models(tile)

        obstacle = self.initial_tile.get_obstacle_in_direction(d)
        if isinstance(obstacle, WallModel):
            status = obstacle.wall_status()
            if status is WallStatusEnum.INTACT:  # checks whether wall is intact
                obstacle.inflict_damage()  # make it damaged.
                damage = self.game_state.damage
                self.game_state.damage = damage + 1  # increment damage count.

            elif status is WallStatusEnum.DAMAGED:  # checks if wall is damaged
                obstacle.inflict_damage()
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
