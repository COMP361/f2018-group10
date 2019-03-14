from src.action_events.action_event import ActionEvent
from src.constants.state_enums import SpaceStatusEnum, POIIdentityEnum, VictimStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class ReplenishPOIEvent(ActionEvent):

    def __init__(self, seed: int):
        super().__init__()
        self.seed = seed
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board

    # Use this method to check whether
    # the POIs should be replenished or not
    def check(self):
        num_active_pois = len(self.board.active_pois)
        print(f"There are currently {num_active_pois} active poi's")
        if num_active_pois >= 3:
            return False

        return True

    def execute(self):
        print("Executing ReplenishPOIEvent")
        if not self.check():
            print("There are more than 3 poi's active, don't need to replenish.")
            return

        num_pois_to_add = 3 - len(self.board.active_pois)
        print(f"Must add {num_pois_to_add} poi's")
        x = 0
        while x < num_pois_to_add and len(self.board.poi_bank) > 0:

            new_poi_row = self.game.roll_red_dice(self.seed)
            new_poi_column = self.game.roll_black_dice(self.seed)
            tile = self.board.get_tile_at(new_poi_row, new_poi_column)
            new_poi = self.board.get_random_poi_from_bank(self.seed)
            print(f"Placing new poi on location: {new_poi_row}, {new_poi_column}")
            new_poi.set_pos(tile.row, tile.column)

            # if the tile already has a POI on it, reroll.
            # (do this by decrementing x so that one more
            # iteration happens and skip the current iteration)
            do_reroll = False
            for assoc_model in tile.associated_models:
                if isinstance(assoc_model, POIModel) or isinstance(assoc_model, VictimModel):
                    do_reroll = True
                    break

            if do_reroll:
                print("Tile already had a POI. Rerolling.")
                continue

            # if tile has smoke/fire, remove it
            # and then add the new poi
            if tile.space_status != SpaceStatusEnum.SAFE:
                print("Tile was not SAFE for adding POI. It is now safe.")
                tile.space_status = SpaceStatusEnum.SAFE

            tile.add_associated_model(new_poi)
            self.game.game_board.add_poi_or_victim(new_poi)

            # if tile has a fireman on it, immediately flip
            # the POI and remove it if it is a False Alarm
            players_on_tile = self.game.get_players_on_tile(tile.row, tile.column)
            if len(players_on_tile) > 0:
                new_victim = None
                tile.remove_associated_model(new_poi)
                self.game.game_board.remove_poi_or_victim(new_poi)
                if new_poi.identity == POIIdentityEnum.FALSE_ALARM:
                    print("POI was placed on a player and was false alarm. Placing another poi")
                    # Need one more iteration since we
                    # just removed the added POI
                    x -= 1
                else:
                    # Add a victim in place of the POI
                    new_victim = VictimModel(VictimStateEnum.ON_BOARD)
                    tile.add_associated_model(new_victim)
                    self.game.game_board.add_poi_or_victim(new_victim)
                    print("POI was placed on a player and was a victim. It has been revealed.")
                new_poi.reveal(new_victim)
            x += 1
            self.game.game_board.active_pois.remove(new_poi)

