from src.action_events.action_event import ActionEvent
from src.action_events.knock_down_event import KnockDownEvent
from src.constants.state_enums import WallStatusEnum, SpaceStatusEnum, SpaceKindEnum, VictimStateEnum, DoorStatusEnum, \
    POIStatusEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.null_model import NullModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class AdvanceFireEvent(ActionEvent):
    """

    $$$$$$$$$$$$$$$$$$$$

    DO NOT USE: SEE EndTurnAdvanceFireEvent instead.

    $$$$$$$$$$$$$$$$$$$$

    """
    def __init__(self, red_dice: int = None, black_dice: int = None):
        super().__init__()
        self.game_state: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game_state.game_board
        self.initial_tile: TileModel = None
        self.red_dice = red_dice
        self.black_dice = black_dice

        # Pick random location: roll dice
        if not self.red_dice:
            self.red_dice = self.game_state.roll_red_dice()
        if not self.black_dice:
            self.black_dice = self.game_state.roll_black_dice()
        self.directions = ["North", "South", "East", "West"]

    def execute(self, *args, **kwargs):
        # Change state of tile depending on previous state
        self.initial_tile = self.board.get_tile_at(self.red_dice, self.black_dice)
        self.advance_on_tile(self.initial_tile)
        self.flashover()
        self.affect_damages()

    def advance_on_tile(self, target_tile: TileModel):
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
                self.game_state.damage = self.game_state.damage + 1

            # fire does not move to the neighbouring tile
            # removing door that borders the tile
            elif isinstance(obstacle, DoorModel):
                obstacle.destroy_door()

            # fire can move to the neighbouring tile
            # if the neighbouring tile is on fire, a shockwave is created
            # else it is just set on fire.
            else:
                nb_tile = origin_tile.get_tile_in_direction(direction)
                if not isinstance(nb_tile, NullModel):
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
            #   1. if neighbouring tile is not on fire, set it to fire
            #       and stop the shockwave.
            #   2. else set the current tile to the neighbouring tile
            #       and continue the shockwave.
            if not tile.has_obstacle_in_direction(direction):
                nb_tile: TileModel = tile.get_tile_in_direction(direction)
                if nb_tile.space_status != SpaceStatusEnum.FIRE:
                    nb_tile.space_status = SpaceStatusEnum.FIRE
                    should_stop = True

                else:
                    tile = nb_tile

            # if there is an obstacle in the given direction
            else:
                # 1. if obstacle is a wall, inflict damage on it, increment
                #   game state damage and stop the shockwave.
                # 2. if obstacle is an open door, continue the shockwave
                #   and destroy the door.
                # 3. if obstacle is a closed door, stop the shockwave
                #   and destroy the door.
                obstacle = tile.get_obstacle_in_direction(direction)
                if isinstance(obstacle, WallModel):
                    obstacle.inflict_damage()
                    self.game_state.damage = self.game_state.damage + 1
                    should_stop = True

                elif isinstance(obstacle, DoorModel):
                    if obstacle.door_status == DoorStatusEnum.CLOSED:
                        should_stop = True
                    obstacle.destroy_door()

                else:
                    pass


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
                if isinstance(model, VictimModel):
                    self.game_state.victims_lost = self.game_state.victims_lost + 1
                    model: VictimModel = model
                    model.state = VictimStateEnum.LOST
                    tile.remove_associated_model(model)
                    self.board.remove_poi_or_victim(model)

                elif isinstance(model, POIModel):
                    model.reveal()
                    model.status = POIStatusEnum.LOST
                    tile.remove_associated_model(model)
                    self.board.remove_poi_or_victim(model)

                else:
                    pass

            players_on_tile = self.game_state.get_players_on_tile(tile.row, tile.column)
            for player in players_on_tile:
                KnockDownEvent(player.ip).execute()

        # removing any fire markers that were
        # placed outside of the building
        for tile in self.board.tiles:
            if tile.space_kind != SpaceKindEnum.INDOOR and tile.space_status == SpaceStatusEnum.FIRE:
                tile.space_status = SpaceStatusEnum.SAFE