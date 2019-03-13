from src.action_events.action_event import ActionEvent
from src.constants.state_enums import SpaceStatusEnum, POIIdentityEnum, VictimStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class ReplenishPOIEvent(ActionEvent):

    def __init__(self):
        super().__init__()
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board

    # Use this method to check whether
    # the POIs should be replenished or not
    def check(self):
        num_active_pois = len(self.board.active_pois)
        if num_active_pois >= 3:
            return False

        return True

    def execute(self):
        if not self.check():
            return

        num_pois_to_add = 3 - len(self.board.active_pois)
        for x in range(num_pois_to_add):
            new_poi_row = self.game.roll_red_dice()
            new_poi_column = self.game.roll_black_dice()
            tile = self.board.get_tile_at(new_poi_row, new_poi_column)
            new_poi = self.board.get_random_poi_from_bank()

            # if the tile already has a POI on it, reroll.
            # (do this by decrementing x so that one more
            # iteration happens and skip the current iteration)
            do_reroll = False
            for assoc_model in tile.associated_models:
                if isinstance(assoc_model, POIModel) or isinstance(assoc_model, VictimModel):
                    x -= 1
                    do_reroll = True
                    break

            if do_reroll:
                continue

            # if tile has smoke/fire, remove it
            # and then add the new poi
            if tile.space_status != SpaceStatusEnum.SAFE:
                tile.space_status = SpaceStatusEnum.SAFE

            tile.add_associated_model(new_poi)
            self.game.game_board.add_poi_or_victim(new_poi)

            # if tile has a fireman on it, immediately flip
            # the POI and remove it if it is a False Alarm
            players_on_tile = self.game.get_players_on_tile(tile.row, tile.column)
            if len(players_on_tile) > 0:
                new_poi.reveal()
                tile.remove_associated_model(new_poi)
                self.game.game_board.remove_poi_or_victim(new_poi)
                if new_poi.identity == POIIdentityEnum.FALSE_ALARM:
                    # Need one more iteration since we
                    # just removed the added POI
                    x -= 1
                else:
                    # Add a victim in place of the POI
                    new_victim = VictimModel(VictimStateEnum.ON_BOARD)
                    tile.add_associated_model(new_victim)
                    self.game.game_board.add_poi_or_victim(new_victim)
