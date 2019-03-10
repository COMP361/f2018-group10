from src.action_events.action_event import ActionEvent
from src.constants.state_enums import SpaceStatusEnum, POIIdentityEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class ReplenishPOIEvent(ActionEvent):

    def __init__(self):
        super().__init__()
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board

    def execute(self):
        num_active_pois = len(self.board.active_pois)
        # TODO: Start here - This is the precondition code - Move it to the GUI
        if num_active_pois >= 3:
            return
        # TODO: End here

        num_pois_to_add = 3 - num_active_pois
        for x in range(num_pois_to_add):
            new_poi_row = self.game.roll_red_dice()
            new_poi_column = self.game.roll_black_dice()
            tile = self.board.get_tile_at(new_poi_row, new_poi_column)
            new_poi = self.board.get_random_poi_from_bank()
            is_added = False

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
                is_added = True

            # if tile has a fireman on it, immediately flip
            # the POI and remove it if it is a False Alarm
            for assoc_model in tile.associated_models:
                if isinstance(assoc_model, PlayerModel):
                    if not is_added:
                        tile.add_associated_model(new_poi)
                        is_added = True

                    new_poi.reveal()
                    if new_poi.identity == POIIdentityEnum.FALSE_ALARM:
                        tile.remove_associated_model(new_poi)

                    break
