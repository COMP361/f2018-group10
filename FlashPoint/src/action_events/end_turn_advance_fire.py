import random
import logging
import time

import threading
from threading import Thread

import src.core.pause_event_switch as switch

from src.UIComponents.file_importer import FileImporter
from src.action_events.knock_down_event import KnockDownEvent
from src.action_events.replenish_poi_event import ReplenishPOIEvent
from src.constants.custom_event_enums import CustomEventEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_board.door_model import DoorModel
from src.models.game_board.null_model import NullModel
from src.models.game_board.wall_model import WallModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.game_board_model import GameBoardModel
from src.constants.state_enums import GameStateEnum, SpaceStatusEnum, WallStatusEnum, DoorStatusEnum, VictimStateEnum, \
    SpaceKindEnum, POIIdentityEnum, GameKindEnum, PlayerRoleEnum
from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard
from src.constants.media_constants import EXPLOSION_SOUND

logger = logging.getLogger("FlashPoint")


class EndTurnAdvanceFireEvent(TurnEvent):
    """
    Event that updates the game state at the end of a turn.

    Steps:
        1)start the AdvanceFire
        2)knockdown event
        3)replenish POI
        4)retain and replenish player's AP
        5)call player_next

     A seed for the random number generator is used to make sure that random numbers stay consistent across machines.
     The person who ended their turn sets the seed, then all other players will see that the seed has already been
     set, and simply use it instead of setting their own. Once the seed has been set, it is set forever, globally.
     Calls to random.seed(seed) will reset the seed.

    """
    def __init__(self, seed: int = 0):
        super().__init__()
        self.player: PlayerModel = GameStateModel.instance().players_turn
        self.initial_tile: TileModel = None

        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

    def _main_phase_end_turn(self):
        # ------ AdvanceFire ------ #
        # Change state of tile depending on previous state

        # Assume that a Flare Up will occur so that we iterate
        # through the loop at least once (like a do-while loop).
        # Advance on tile will decide whether a flare up will
        # occur or not and whether we should roll the dice once more.
        flare_up_will_occur = True
        x = 0
        while flare_up_will_occur:
            # Will log if a flare up was actually caused
            # (skips the first default iteration)
            if x > 0:
                logger.info("Flare up triggered by {tile}".format(tile=self.initial_tile))
            self.initial_tile = self.board.get_tile_at(self.red_dice, self.black_dice)
            flare_up_will_occur = self.advance_on_tile(self.initial_tile)
            self.flashover()
            self.resolve_hazmat_explosions()
            # Preparing the dice for the next
            # iteration if a flare up is going to occur
            self.red_dice = self.game_state.roll_red_dice()
            self.black_dice = self.game_state.roll_black_dice()
            x += 1

        self.affect_damages()
        # Add a hotspot marker to the last
        # target space of the advance_on_tile()
        if self.board.hotspot_bank > 0 and x > 1:
            self.initial_tile.is_hotspot = True
            self.board.hotspot_bank = self.board.hotspot_bank - 1

        # ------ ReplenishPOI ------ #
        rp_event = ReplenishPOIEvent(self.seed)
        rp_event.execute()

        # ------ Replenish Player's points ----- #
        self._replenish_player_points()

    def _replenish_player_points(self):
        """
        Replenishes a player's AP, special AP
        according to the rules for the different roles.

        :return:
        """
        # retain up to a maximum of 4 AP
        # as the turn is ending and
        # replenish player's AP, irrespective
        # of role, by 4 (add/subtract points after).
        # special AP are not retained for the next turn.
        # Handle Doge's case separately...
        if self.player.role == PlayerRoleEnum.DOGE:
            if self.player.ap > 6:
                self.player.ap = 6

            self.player.ap = self.player.ap + 12
            self._take_away_AP_given_by_veteran()
            return

        if self.player.ap > 4:
            self.player.ap = 4

        self.player.ap = self.player.ap + 4

        if self.player.role == PlayerRoleEnum.CAPTAIN:
            self.player.special_ap = 2

        elif self.player.role == PlayerRoleEnum.CAFS:
            self.player.ap = self.player.ap - 1
            self.player.special_ap = 3

        elif self.player.role == PlayerRoleEnum.GENERALIST:
            self.player.ap = self.player.ap + 1

        elif self.player.role == PlayerRoleEnum.RESCUE:
            self.player.special_ap = 3

        else:
            pass

        self._take_away_AP_given_by_veteran()

    def _take_away_AP_given_by_veteran(self):
        if self.player.has_AP_from_veteran:
            if self.player.ap > 0:
                logger.info("Taking away free AP given by Veteran to Player at ({r}, {c})".format(r=self.player.row, c=self.player.column))
                self.player.ap = self.player.ap - 1
            self.player.has_AP_from_veteran = False

    def _placing_players_end_turn(self):
        # If the last player has chosen a location, move the game into the next phase.
        if self.game_state.rules == GameKindEnum.EXPERIENCED:
            logger.info("Game phase has moved to PLACING_VEHICLES")
            self.game_state.state = GameStateEnum.PLACING_VEHICLES
        else:
            logger.info("Game phase has moved to MAIN_GAME")
            self.game_state.state = GameStateEnum.MAIN_GAME

    def _placing_vehicles_end_turn(self):
        # Don't call the next player. Wait until the host chooses the positions.
        if self.game_state.vehicles_have_been_placed():
            logger.info("Game phase has moved to MAIN_GAME")
            self.game_state.state = GameStateEnum.MAIN_GAME
        else:
            logger.info("Not all vehicles have been placed. Not moving to next game phase.")

    def execute(self):
        self.game_state: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game_state.game_board
        logger.info("Executing EndTurnAdvanceFireEvent")

        # Pick random location: roll dice
        random.seed(self.seed)

        self.red_dice = GameStateModel.instance().roll_red_dice()
        self.black_dice = GameStateModel.instance().roll_black_dice()
        self.directions = ["North", "South", "East", "West"]

        # Clear commanded list
        self.game_state.clear_commanded_list()

        if self.game_state.state == GameStateEnum.MAIN_GAME:
            self._main_phase_end_turn()

        elif self.game_state.state == GameStateEnum.PLACING_PLAYERS:
            if self.game_state.all_players_have_chosen_location():
                self._placing_players_end_turn()
            else:
                logger.info("Not all players have chosen starting location, not moving to next game phase.")
                if not self.game_state.players_turn.has_pos:
                    logger.info("The player did not choose a location, not moving to next player.")
                    self.game_state._notify_player_index()
                    return

        elif self.game_state.state == GameStateEnum.PLACING_VEHICLES:
            self._placing_vehicles_end_turn()
            self.game_state._notify_player_index()
            return

        # call next player
        self.game_state.next_player()

    def advance_on_tile(self, target_tile: TileModel) -> bool:
        """
        Advances the fire on the target tile.
        Determines whether a flare up should
        occur or not after this instance of
        Advance Fire is done.

        :param target_tile:
        :return: boolean which tells us if a flare up will occur
        """
        flare_up_will_occur = False
        if target_tile.is_hotspot:
            flare_up_will_occur = True

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

        return flare_up_will_occur

    def explosion(self, origin_tile: TileModel):
        FileImporter.play_music(EXPLOSION_SOUND, 1)
        logger.info(f"Explosion occurred on {origin_tile}")
        game_state = GameStateModel.instance()
        tile_sprite = GameBoard.instance().grid.grid[origin_tile.column][origin_tile.row]
        tile_sprite.explosion = True

        for direction, obstacle in origin_tile.adjacent_edge_objects.items():
            # fire does not move to the neighbouring tile
            # damaging wall present along the tile
            if isinstance(obstacle, WallModel) and obstacle.wall_status != WallStatusEnum.DESTROYED:
                obstacle.inflict_damage()
                game_state.damage = game_state.damage + 1

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
        game_state = GameStateModel.instance()
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
                    game_state.damage = game_state.damage + 1
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

    def resolve_hazmat_explosions(self):
        """
        For all the fire tiles, if any of them
        contain a hazmat, cause an explosion
        in that space. After the explosion,
        remove the hazmat from the tile and
        put a hotspot marker on that tile.

        :return:
        """
        for tile in self.game_state.game_board.tiles:
            if tile.space_status == SpaceStatusEnum.FIRE:
                # If the tile contains a Hazmat, trigger
                # an explosion.
                for assoc_model in tile.associated_models:
                    if isinstance(assoc_model, HazmatModel):
                        logger.info("Hazmat explosion occured on {t}".format(t=tile))
                        self.explosion(tile)
                        assoc_model.set_pos(-7, -7)
                        tile.remove_associated_model(assoc_model)
                        if self.board.hotspot_bank > 0:
                            tile.is_hotspot = True
                            self.board.hotspot_bank = self.board.hotspot_bank - 1

                # If there are any players on the tile and
                # if they are carrying a Hazmat, knock down
                # the player, trigger an explosion and disassociate
                # the Hazmat from the player.
                players_on_tile = self.game_state.get_players_on_tile(tile.row, tile.column)
                for player in players_on_tile:
                    if isinstance(player.carrying_hazmat, HazmatModel):
                        logger.info("Hazmat explosion occured on {t}".format(t=tile))
                        self.explosion(tile)
                        if not self.dodge(player):
                            KnockDownEvent(player.ip).execute()
                        player.carrying_hazmat.set_pos(-7, -7)
                        player.carrying_hazmat = NullModel()
                        if self.board.hotspot_bank > 0:
                            tile.is_hotspot = True
                            self.board.hotspot_bank = self.board.hotspot_bank - 1

    def countdown(self):
        EventQueue.post(CustomEvent(CustomEventEnum.ENABLE_VICTIM_LOST_PROMPT))
        time.sleep(5)
        EventQueue.post(CustomEvent(CustomEventEnum.DISABLE_VICTIM_LOST_PROMPT))

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
                    logger.info(f"{model} was lost.")

                    thread = Thread(target=self.countdown)
                    thread.start()
                    self.game_state.victims_lost = self.game_state.victims_lost + 1
                    model: VictimModel = model
                    model.state = VictimStateEnum.LOST
                    tile.remove_associated_model(model)
                    self.board.remove_poi_or_victim(model)

                elif isinstance(model, POIModel):
                    # Reveal the POI and remove it regardless
                    # of False Alarm or Victim identity.
                    # If it is a Victim, put a Victim model
                    # there, sleep (inside remove_poi_or_victim)
                    # so that the victim can be seen briefly, then
                    # remove it and increment the game state damage.
                    new_victim = None
                    model.reveal(new_victim)
                    tile.remove_associated_model(model)
                    self.board.remove_poi_or_victim(model)
                    if model.identity == POIIdentityEnum.VICTIM:
                        new_victim = VictimModel(VictimStateEnum.ON_BOARD)
                        tile.add_associated_model(new_victim)
                        self.board.add_poi_or_victim(new_victim)
                        tile.remove_associated_model(new_victim)
                        self.board.remove_poi_or_victim(new_victim)
                        self.game_state.victims_lost = self.game_state.victims_lost + 1
                        logger.info(f"{new_victim} was lost.")
                    logger.info(f"{model} was removed from the game.")
                else:
                    pass

            players_on_tile = self.game_state.get_players_on_tile(tile.row, tile.column)
            for player in players_on_tile:
                # Attempt to dodge and if it doesn't
                # work, the player gets knocked down
                if not self.dodge(player):
                    KnockDownEvent(player.ip).execute()

        # removing any fire markers that were
        # placed outside of the building
        for tile in self.board.tiles:
            if tile.space_kind != SpaceKindEnum.INDOOR and tile.space_status == SpaceStatusEnum.FIRE:
                tile.space_status = SpaceStatusEnum.SAFE

    def dodge(self, player: PlayerModel) -> bool:
        """
        Determines whether the player can
        dodge (out of turn) to avoid being
        knocked down and performs dodge.
        Returns False otherwise.

        :param player: player that is attempting to dodge
        :return: True if the player is able to dodge, False otherwise
        """
        logger.info("Attempting to dodge...")
        # Doge cannot dodge
        if player.role == PlayerRoleEnum.DOGE:
            self._log_player_dodge(1, player)
            return False

        if not self._valid_to_dodge(player):
            self._log_player_dodge(1, player)
            return False

        player_tile = self.game_state.game_board.get_tile_at(player.row, player.column)
        possible_dodge_target = NullModel()
        for dirn, nb_tile in player_tile.adjacent_tiles.items():
            if isinstance(nb_tile, TileModel):
                has_obstacle = player_tile.has_obstacle_in_direction(dirn)
                obstacle = player_tile.get_obstacle_in_direction(dirn)
                is_open_door = isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.OPEN
                if not has_obstacle or is_open_door:
                    if nb_tile.space_status != SpaceStatusEnum.FIRE:
                        possible_dodge_target = nb_tile
                        break

        # If we couldn't find a potential space
        # to dodge, the player cannot avoid being
        # knocked down.
        if isinstance(possible_dodge_target, NullModel):
            self._log_player_dodge(1, player)
            return False

        # Pause the current event and ask player to dodge:
        EventQueue.post(CustomEvent(CustomEventEnum.DODGE_PROMPT, player))
        logger.info(f"Thread {threading.current_thread().getName()} going to sleep")
        # Go to sleep
        switch.pause_event.clear()
        switch.pause_event.wait()
        logger.info(f"Thread {threading.current_thread().getName()} woke up")
        if not GameStateModel.instance().dodge_reply:
            logger.info("Reply was no, knocking player down")
            return False

        logger.info("Reply was yes, attempting to dodge...")
        GameStateModel.instance().dodge_reply = False
        # Disassociate the victim/hazmat that the player
        # may be carrying since they cannot dodge with them
        player_victim = player.carrying_victim
        player_hazmat = player.carrying_hazmat
        is_carrying_victim = isinstance(player_victim, VictimModel)
        is_carrying_hazmat = isinstance(player_hazmat, HazmatModel)
        if is_carrying_victim:
            self._log_player_dodge(2, player, player_victim, player_tile)
            player_tile.add_associated_model(player_victim)
            player.carrying_victim = NullModel()

        if is_carrying_hazmat:
            self._log_player_dodge(2, player, player_hazmat, player_tile)
            player_tile.add_associated_model(player_hazmat)
            player.carrying_hazmat = NullModel()

        self._log_player_dodge(3, player)
        player.set_pos(possible_dodge_target.row, possible_dodge_target.column)
        # Costs 1 AP for Veteran to dodge
        # and 2 AP for the rest of the roles
        if player.role == PlayerRoleEnum.VETERAN:
            player.ap = player.ap - 1
        else:
            player.ap = player.ap - 2

        return True

    def _log_player_dodge(self, status: int, player: PlayerModel, model = None, tile: TileModel = None):
        """
        Log player information while
        attempting to dodge.

        :param status:
            1 - cannot dodge
            2 - disassociating model
            3 - able to dodge
        :param player:
        :param model:
        :return:
        """
        r = player.row
        c = player.column
        if status == 1:
            logger.info("Player at ({row}, {col}) cannot dodge".format(row=r, col=c))

        elif status == 2:
            logger.info("Disassociate {m} from Player at ({row}, {col}) and give it to {t}".format(m=model, row=r, col=c, t=tile))

        elif status == 3:
            logger.info("Player at ({row}, {col}) is able to dodge".format(row=r, col=c))

        return

    def _valid_to_dodge(self, player: PlayerModel) -> bool:
        """
        Determines whether the player can dodge
        based on their role, saved AP and
        permission to dodge.

        :param player: player who is trying to dodge
        :return: True if they have enough AP to dodge, False otherwise.
        """
        # Only the Veteran is allowed to dodge at
        # all times. The rest of the roles can only
        # dodge when they are in the vicinity of the Veteran.
        if player.role != PlayerRoleEnum.VETERAN:
            if not player.allowed_to_dodge:
                return False

        # The player must have at least replenished AP + 1 saved AP
        # (for Veteran) or 2 saved AP (for other roles) to be able to dodge.

        # Needs at least 1 saved AP
        if player.role == PlayerRoleEnum.VETERAN:
            if player.ap < 1:
                return False

        # All of the ones below need at least 2 saved AP
        elif player.role in [PlayerRoleEnum.PARAMEDIC, PlayerRoleEnum.CAPTAIN, PlayerRoleEnum.IMAGING,
                             PlayerRoleEnum.HAZMAT, PlayerRoleEnum.DRIVER, PlayerRoleEnum.RESCUE]:
            if player.ap < 2:
                return False

        elif player.role == PlayerRoleEnum.CAFS:
            if player.ap < 2:
                return False

        elif player.role == PlayerRoleEnum.GENERALIST:
            if player.ap < 2:
                return False

        else:
            pass

        return True
