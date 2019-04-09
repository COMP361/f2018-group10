import enum
import json

from typing import Dict, List
import logging

from src.action_events.board_setup_event import BoardSetupEvent
from src.action_events.disconnect_event import DisconnectEvent
from src.action_events.dodge_reply_event import DodgeReplyEvent
from src.action_events.end_game_event import EndGameEvent
from src.action_events.fire_placement_event import FirePlacementEvent
from src.action_events.choose_character_event import ChooseCharacterEvent
from src.action_events.random_board_setup_event import RandomBoardSetupEvent
from src.action_events.turn_events.drop_hazmat_event import DropHazmatEvent
from src.action_events.turn_events.lead_victim_event import LeadVictimEvent
from src.action_events.turn_events.pick_up_hazmat_event import PickupHazmatEvent
from src.action_events.turn_events.fire_deck_gun_event import FireDeckGunEvent
from src.action_events.turn_events.remove_hazmat_event import RemoveHazmatEvent
from src.action_events.turn_events.identify_poi_event import IdentifyPOIEvent
from src.action_events.place_hazmat_event import PlaceHazmatEvent
from src.action_events.end_turn_advance_fire import EndTurnAdvanceFireEvent
from src.action_events.set_initial_hotspot_event import SetInitialHotspotEvent
from src.action_events.set_initial_poi_experienced_event import SetInitialPOIExperiencedEvent
from src.action_events.set_initial_poi_family_event import SetInitialPOIFamilyEvent
from src.action_events.turn_events.chop_event import ChopEvent
from src.action_events.turn_events.close_door_event import CloseDoorEvent
from src.action_events.turn_events.dismount_vehicle_event import DismountVehicleEvent
from src.action_events.turn_events.drive_vehicle_event import DriveVehicleEvent
from src.action_events.turn_events.drop_victim_event import DropVictimEvent
from src.action_events.turn_events.extinguish_event import ExtinguishEvent
from src.action_events.turn_events.move_event import MoveEvent
from src.action_events.turn_events.pick_up_victim_event import PickupVictimEvent
from src.action_events.turn_events.open_door_event import OpenDoorEvent
from src.action_events.turn_events.resuscitate_victim_event import ResuscitateEvent
from src.action_events.turn_events.ride_vehicle_event import RideVehicleEvent
from src.action_events.turn_events.stop_leading_victim_event import StopLeadingVictimEvent
from src.action_events.vehicle_placed_event import VehiclePlacedEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.null_model import NullModel
from src.models.game_board.wall_model import WallModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel
from src.models.model import Model
from src.observers.observer import Observer
from src.models.game_board.tile_model import TileModel
from src.action_events.turn_events.choose_starting_position_event import ChooseStartingPositionEvent
from src.action_events.start_game_event import StartGameEvent
from src.action_events.ready_event import ReadyEvent
from src.action_events.chat_event import ChatEvent
from src.action_events.dummy_event import DummyEvent
from src.action_events.join_event import JoinEvent
from src.constants.state_enums import DifficultyLevelEnum, GameKindEnum, PlayerStatusEnum, WallStatusEnum, \
    DoorStatusEnum, SpaceKindEnum, SpaceStatusEnum, ArrowDirectionEnum, PlayerRoleEnum, GameBoardTypeEnum, \
    POIIdentityEnum, POIStatusEnum, GameStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.sprites.hazmat_sprite import HazmatSprite

logger = logging.getLogger("FlashPoint")

class EndTurnEvent(object):
    pass


class JSONSerializer(object):
    """Used for serializing and deserializing objects to JSON."""

    @staticmethod
    def _deserialize_game_state(payload: Dict) -> GameStateModel:
        """Deserialize a game state"""
        host: PlayerModel = JSONSerializer.deserialize(payload['_host'])

        num_players = payload['_max_desired_players']
        rules = GameKindEnum(payload['_rules']["value"])
        board_type = GameBoardTypeEnum(payload['_board_type']["value"])
        difficulty_level = None
        if rules == GameKindEnum.EXPERIENCED:
            difficulty_level = DifficultyLevelEnum(payload['_difficulty_level']['value'])

        if not GameStateModel.instance():
            game = GameStateModel(host, num_players, rules, board_type, difficulty_level)
        else:
            game = GameStateModel.instance()

        for player in [x for x in payload['_players'] if x['_ip'] != host.ip]:
            player_obj: PlayerModel = JSONSerializer.deserialize(player)
            if player_obj not in game.players:
                game.add_player(player_obj)

        JSONSerializer.restore_game_board(game, payload['_game_board'])
        game.players_turn = payload['_players_turn_index']
        game.damage = payload['_damage']
        game.max_damage = payload['_max_damage']
        game.victims_lost = payload['_victims_lost']
        game.victims_saved = payload['_victims_saved']

        return game


    @staticmethod
    def _restore_carried_hazmats(game: GameStateModel):
        """Helper for restoring GameBoardModel"""
        picked_up_hazmats = [player.carrying_hazmat for player in game.players
                             if not isinstance(player.carrying_hazmat, NullModel)]

        for hazmat in picked_up_hazmats:
            tile = game.game_board.get_tile_at(hazmat.row, hazmat.column)
            tile.add_associated_model(hazmat)

    @staticmethod
    def _restore_carried_victims(game: GameStateModel):
        """Helper for restoring GameBoardModel"""
        picked_up_victims = [player.carrying_victim for player in game.players
                             if not isinstance(player.carrying_victim, NullModel)]
        for victim in picked_up_victims:
            tile = game.game_board.get_tile_at(victim.row, victim.column)
            tile.add_associated_model(victim)
            game.game_board.active_pois.append(victim)

    @staticmethod
    def _restore_tile_state(game: GameStateModel, payload: Dict):
        """Restore the full state of all tiles, including associated models and sprites."""
        for row in range(len(payload['_tiles'])):
            for column in range(len(payload['_tiles'][row])):
                tile_dict = payload['_tiles'][row][column]
                tile = game.game_board.get_tile_at(row, column)
                tile.space_status = SpaceStatusEnum(tile_dict['_space_status']['value'])
                tile.space_kind = SpaceKindEnum(tile_dict['_space_kind']['value'])
                tile.is_hotspot = tile_dict['_is_hotspot']

                for assoc_model_dict in tile_dict['_associated_models']:
                    model: Model = JSONSerializer.deserialize(assoc_model_dict)
                    tile.add_associated_model(model)
                    if isinstance(model, VictimModel) or isinstance(model, POIModel):
                        game.game_board.active_pois.append(model)

    @staticmethod
    def _restore_wall_and_door_states(game: GameStateModel, payload: Dict):
        """Restore all the states of all the walls. Must be called """
        for row in range(len(payload['_tiles'])):
            for column in range(len(payload['_tiles'][row])):
                tile_dict = payload['_tiles'][row][column]
                tile = game.game_board.get_tile_at(row, column)

                east_obj = tile.adjacent_edge_objects["East"]
                south_obj = tile.adjacent_edge_objects["South"]

                if isinstance(east_obj, WallModel):
                    wall_dict = tile_dict['_adjacent_edge_objects']["East"]
                    east_obj.wall_status = WallStatusEnum(wall_dict['_wall_status']['value'])
                elif isinstance(east_obj, DoorModel):
                    door_dict = tile_dict['_adjacent_edge_objects']["East"]
                    east_obj.door_status = DoorStatusEnum(door_dict['_door_status']['value'])

                if isinstance(south_obj, WallModel):
                    wall_dict = tile_dict['_adjacent_edge_objects']["South"]
                    south_obj.wall_status = WallStatusEnum(wall_dict['_wall_status']['value'])
                elif isinstance(south_obj, DoorModel):
                    door_dict = tile_dict['_adjacent_edge_objects']["South"]
                    south_obj.door_status = DoorStatusEnum(door_dict['_door_status']['value'])

    @staticmethod
    def _restore_parking_spots(game: GameStateModel, payload: Dict):
        a_spots_dict = payload['_ambulance_spots']
        e_spots_dict = payload['_engine_spots']
        a_spots = []
        e_spots = []

        def fill_spots_list(spots_dict, spots_list):
            for spot in spots_dict:
                first_tile = game.game_board.get_tile_at(spot[0]['_row'], spot[0]['_column'])
                second_tile = game.game_board.get_tile_at(spot[1]['_row'], spot[1]['_column'])
                spots_list.append([first_tile, second_tile])

        fill_spots_list(a_spots_dict, a_spots)
        fill_spots_list(e_spots_dict, e_spots)

        game.game_board.ambulance_spots = a_spots
        game.game_board.engine_spots = e_spots

    @staticmethod
    def _restore_poi_bank(game: GameStateModel, payload: Dict):
        poi_bank_dict = payload['_poi_bank']

        bank = []
        for poi_dict in poi_bank_dict:
            bank.append(JSONSerializer.deserialize(poi_dict))

        game.game_board.poi_bank = bank

    @staticmethod
    def restore_game_board(game: GameStateModel, payload: Dict):
        """Special deserialize called from the GameStateModel deserializer."""
        if payload['_board_info']:
            game.game_board = GameBoardModel(GameBoardTypeEnum.RANDOM, payload['_board_info'])
        JSONSerializer._restore_carried_hazmats(game)
        JSONSerializer._restore_carried_victims(game)
        JSONSerializer._restore_tile_state(game, payload)
        JSONSerializer._restore_parking_spots(game, payload) # Might not be necessary but oh well.
        JSONSerializer._restore_wall_and_door_states(game, payload)
        JSONSerializer._restore_poi_bank(game, payload)
        game.game_board.hotspot_bank = payload['_hotspot_bank']

    @staticmethod
    def _deserialize_player(payload: Dict) -> PlayerModel:
        ip = payload["_ip"]
        nickname = payload['_nickname']

        player = PlayerModel(ip, nickname)
        #player.set_pos(payload['_row'], payload['_column'])
        player.set_pos(0,0)
        player.color = tuple(payload['_color'])
        player.status = PlayerStatusEnum(payload["_status"]["value"])
        player.ap = payload['_ap']
        player.special_ap = payload['_special_ap']
        player.wins = payload['_wins']
        player.losses = payload['_losses']
        player.role = PlayerRoleEnum(payload["_role"]["value"])
        if payload['_carrying_hazmat']:
            player.carrying_hazmat = JSONSerializer.deserialize(payload['_carrying_hazmat'])
        if payload['_carrying_victim']:
            player.carrying_victim = JSONSerializer.deserialize(payload['_carrying_victim'])
        if payload['_leading_victim']:
            player.leading_victim = JSONSerializer.deserialize(payload['_leading_victim'])
        return player

    @staticmethod
    def _deserialize_victim(payload) -> VictimModel:
        victim_state = payload['_state']
        serialized_victim: VictimModel = VictimModel(victim_state)
        serialized_victim.set_pos(payload['_row'], payload['_column'])

        return serialized_victim

    @staticmethod
    def _deserialize_hazmat(payload: Dict) -> HazmatModel:
        hazmat = HazmatModel()
        hazmat.set_pos(payload['_row'], payload['_column'])
        return hazmat

    @staticmethod
    def _deserialize_poi_model(payload: Dict) -> POIModel:
        poi = POIModel(POIIdentityEnum(payload['_identity']['value']))
        poi.set_pos(payload['_row'], payload['_column'])
        poi.status = POIStatusEnum(payload['_status']['value'])
        return poi

    @staticmethod
    def _deserialize_chat_event(payload: Dict) -> ChatEvent:
        message = payload['_message']
        sender = payload['_sender']
        return ChatEvent(message, sender)

    def _deserialize_end_game_event(payload:Dict) -> EndGameEvent:
        state = GameStateEnum(payload['_state']['value'])
        return EndGameEvent(state)

    @staticmethod
    def _deserialize_ready_event(payload: Dict) -> ReadyEvent:
        player: PlayerModel = JSONSerializer.deserialize(payload['_player'])
        ready: bool = payload['_ready']
        return ReadyEvent(player, ready)

    @staticmethod
    def _deserialize_choose_character_event(payload:Dict) -> ChooseCharacterEvent:
        player:PlayerModel = JSONSerializer.deserialize(payload['_player'])
        role = PlayerRoleEnum(payload['_role']['value'])
        return ChooseCharacterEvent(role, player)

    @staticmethod
    def _deserialize_join_event(payload: Dict) -> JoinEvent:
        player = JSONSerializer._deserialize_player(payload['player'])
        return JoinEvent(player)

    @staticmethod
    def _deserialize_choose_position_event(payload: Dict):
        return ChooseStartingPositionEvent(payload['_row'], payload['_column'])

    @staticmethod
    def _deserialize_move_event(payload: Dict):
        game_board = GameStateModel.instance().game_board
        destination = payload['destination']
        tile_list = payload['moveable_tiles']

        moveable_tiles = []
        for tile in tile_list:
            tile_model: TileModel = game_board.get_tile_at(tile['_row'], tile['_column'])
            moveable_tiles.append(tile_model)

        destination_model: TileModel = game_board.get_tile_at(destination['_row'], destination['_column'])
        event = MoveEvent(destination_model, moveable_tiles)
        return event

    @staticmethod
    def _deserialize_tile(payload: Dict) -> TileModel:
        tile: TileModel = TileModel(payload['_row'], payload['_column'], payload['_space_kind'])
        return tile

    @staticmethod
    def _deserialize_door(payload: Dict) -> DoorModel:
        id = payload['_id']
        door = DoorModel(id[0], id[1], id[2], DoorStatusEnum(payload['_door_status']['value']))
        return door

    @staticmethod
    def _deserialize_wall(payload: Dict) -> WallModel:
        id = payload['_id']
        wall = WallModel(id[0], id[1], id[2])
        wall.wall_status = WallStatusEnum(payload['_wall_status']['value'])
        return wall

    @staticmethod
    def _deserialize_door(payload: Dict) -> DoorModel:
        id = payload['_id']
        door = DoorModel(id[0],id[1],id[2])
        door.door_status = DoorStatusEnum(payload['_door_status']['value'])
        return door

    @staticmethod
    def _deserialize_chop_event(payload: Dict) -> ChopEvent:
        wall: WallModel = JSONSerializer.deserialize(payload['wall'])
        return ChopEvent(wall)

    @staticmethod
    def _deserialize_extinguish_event(payload: Dict) -> ExtinguishEvent:
        tile_dict = payload['extinguish_space']
        tile: TileModel = GameStateModel.instance().game_board.get_tile_at(tile_dict['_row'], tile_dict['_column'])
        return ExtinguishEvent(tile)

    @staticmethod
    def _deserialize_open_door_event(payload: Dict) -> OpenDoorEvent:
        door: DoorModel = JSONSerializer.deserialize(payload['door'])
        return OpenDoorEvent(door)

    @staticmethod
    def _deserialize_close_door_event(payload: Dict) -> CloseDoorEvent:
        door: DoorModel = JSONSerializer.deserialize(payload['door'])
        return CloseDoorEvent(door)

    @staticmethod
    def _deserialize_end_turn_advance_fire_event(payload: Dict) -> EndTurnAdvanceFireEvent:
        seed: int = payload['seed']
        event = EndTurnAdvanceFireEvent(seed)
        return event

    @staticmethod
    def _deserialize_drop_victim_event(payload: Dict) -> DropVictimEvent:
        victim_tile: TileModel = JSONSerializer.deserialize(payload['victim_tile'])
        return DropVictimEvent(victim_tile.row, victim_tile.column)

    @staticmethod
    def _deserialize_pickup_victim_event(payload: Dict) -> PickupVictimEvent:
        victim_tile: TileModel = JSONSerializer.deserialize(payload['victim_tile'])
        return PickupVictimEvent(victim_tile.row, victim_tile.column)

    @staticmethod
    def _deserialize_lead_victim_event(payload: Dict) -> LeadVictimEvent:
        victim_tile: TileModel = JSONSerializer.deserialize(payload['victim_tile'])
        return LeadVictimEvent(victim_tile.row, victim_tile.column)

    @staticmethod
    def _deserialize_stop_leading_victim_event(payload: Dict) -> StopLeadingVictimEvent:
        victim_tile: TileModel = JSONSerializer.deserialize(payload['victim_tile'])
        return StopLeadingVictimEvent(victim_tile.row, victim_tile.column)

    @staticmethod
    def _deserialize_drop_hazmat_event(payload: Dict) -> DropHazmatEvent:
        hazmat_tile: TileModel = JSONSerializer.deserialize(payload['hazmat_tile'])
        return DropHazmatEvent(hazmat_tile.row, hazmat_tile.column)

    @staticmethod
    def _deserialize_pickup_hazmat_event(payload: Dict) -> PickupHazmatEvent:
        hazmat_tile: TileModel = JSONSerializer.deserialize(payload['hazmat_tile'])
        return PickupHazmatEvent(hazmat_tile.row, hazmat_tile.column)

    @staticmethod
    def _deserialize_set_initial_poi_family_event(payload: Dict) -> SetInitialPOIFamilyEvent:
        seed = payload['seed']
        return SetInitialPOIFamilyEvent(seed)

    @staticmethod
    def _deserialize_place_hazmat_event(payload: Dict) -> PlaceHazmatEvent:
        seed = payload['seed']
        return PlaceHazmatEvent(seed)

    @staticmethod
    def _deserialize_vehicle_placed_event(payload: Dict) -> VehiclePlacedEvent:
        event: VehiclePlacedEvent = VehiclePlacedEvent()
        event._vehicle_type = payload['_vehicle_type']
        event._row = payload['_row']
        event._column = payload['_column']
        return event

    @staticmethod
    def _deserialize_drive_vehicle_event(payload: Dict) -> DriveVehicleEvent:
        event = DriveVehicleEvent(payload['_vehicle_type'])
        event._row = payload['_row']
        event._column = payload['_column']
        return event

    @staticmethod
    def _deserialize_identify_poi_event(payload: Dict) -> IdentifyPOIEvent:
        event = IdentifyPOIEvent(payload['row'], payload['column'])
        return event

    @staticmethod
    def _deserialize_ride_vehicle_event(payload: Dict) -> RideVehicleEvent:
        player_index = payload['_player_index']
        vehicle_type = payload['_vehicle_type']
        event = RideVehicleEvent(vehicle_type=vehicle_type, player_index=player_index)
        return event

    @staticmethod
    def _deserialize_remove_hazmat_event(payload: Dict) -> RemoveHazmatEvent:
        event = RemoveHazmatEvent(payload['row'], payload['column'])
        return event

    @staticmethod
    def _deserialize_resuscitate_event(payload: Dict) -> RemoveHazmatEvent:
        event = ResuscitateEvent(payload['row'], payload['column'])
        return event

    @staticmethod
    def _deserialize_dismount_vehicle_event(payload: Dict) -> DismountVehicleEvent:
        return DismountVehicleEvent(payload['_vehicle_type'], player_index=payload['_player_index'])

    @staticmethod
    def _deserialize_choose_character_event(payload: Dict) -> ChooseCharacterEvent:
        return ChooseCharacterEvent(PlayerRoleEnum(payload['_role']['value']), payload['_player_index'])

    @staticmethod
    def _deserialize_disconnect_event(payload: Dict) -> DisconnectEvent:
        player: PlayerModel = JSONSerializer.deserialize(payload['_player'])
        return DisconnectEvent(player)

    @staticmethod
    def _deserialize_fire_deck_gun_event(payload: Dict) -> FireDeckGunEvent:
        return FireDeckGunEvent(payload['seed'])

    @staticmethod
    def _deserialize_dodge_reply(payload: Dict) -> DodgeReplyEvent:
        return DodgeReplyEvent(payload['_reply'])

    @staticmethod
    def _deserialize_random_board_event(payload: Dict) -> RandomBoardSetupEvent:
        return RandomBoardSetupEvent(payload['_board_info'])

    @staticmethod
    def deserialize(payload: Dict) -> object:
        """
        Grab an object and deserialize it.
        Note that the object must be able to take a dict as input. If there are nested objects or enums in the object,
        it must define its own _deserialize method by implementing the Serializable abstract class.

        Add to this case statement to be able to deserialize your object type.
        """
        object_type = payload["class"]
        # --------------MODELS----------------
        if object_type == PlayerModel.__name__:
            return JSONSerializer._deserialize_player(payload)
        elif object_type == TileModel.__name__:
            return JSONSerializer._deserialize_tile(payload)
        elif object_type == GameStateModel.__name__:
            return JSONSerializer._deserialize_game_state(payload)
        elif object_type == DoorModel.__name__:
            return JSONSerializer._deserialize_door(payload)
        elif object_type == WallModel.__name__:
            return JSONSerializer._deserialize_wall(payload)
        elif object_type == VictimModel.__name__:
            return JSONSerializer._deserialize_victim(payload)
        elif object_type == HazmatModel.__name__:
            return JSONSerializer._deserialize_hazmat(payload)
        elif object_type == POIModel.__name__:
            return JSONSerializer._deserialize_poi_model(payload)
        # --------------EVENTS------------------
        elif object_type == JoinEvent.__name__:
            return JSONSerializer._deserialize_join_event(payload)
        elif object_type == ChatEvent.__name__:
            return JSONSerializer._deserialize_chat_event(payload)
        elif object_type == ReadyEvent.__name__:
            return JSONSerializer._deserialize_ready_event(payload)
        elif object_type == StartGameEvent.__name__:
            return StartGameEvent()
        elif object_type == EndGameEvent.__name__:
            return JSONSerializer._deserialize_end_game_event(payload)
        elif object_type == EndTurnEvent.__name__:
            return JSONSerializer._deserialize_end_turn_event(payload)
        elif object_type == ChooseStartingPositionEvent.__name__:
            return JSONSerializer._deserialize_choose_position_event(payload)
        elif object_type == ChopEvent.__name__:
            return JSONSerializer._deserialize_chop_event(payload)
        elif object_type == WallModel.__name__:
            return JSONSerializer._deserialize_wall(payload)
        elif object_type == DoorModel.__name__:
            return JSONSerializer._deserialize_door(payload)
        elif object_type == MoveEvent.__name__:
            return JSONSerializer._deserialize_move_event(payload)
        elif object_type == DummyEvent.__name__:
            return DummyEvent()
        elif object_type == DisconnectEvent.__name__:
            return JSONSerializer._deserialize_disconnect_event(payload)
        elif object_type == ExtinguishEvent.__name__:
            return JSONSerializer._deserialize_extinguish_event(payload)
        elif object_type == GameBoardModel.__name__:
            return JSONSerializer._deserialize_game_board(payload)
        elif object_type == NullModel.__name__:
            return NullModel()
        elif object_type == DropVictimEvent.__name__:
            return JSONSerializer._deserialize_drop_victim_event(payload)
        elif object_type == ChooseCharacterEvent.__name__:
            return JSONSerializer._deserialize_choose_character_event(payload)
        elif object_type == PickupVictimEvent.__name__:
            return JSONSerializer._deserialize_pickup_victim_event(payload)
        elif object_type == LeadVictimEvent.__name__:
            return JSONSerializer._deserialize_lead_victim_event(payload)
        elif object_type == StopLeadingVictimEvent.__name__:
            return JSONSerializer._deserialize_stop_leading_victim_event(payload)
        elif object_type == DropHazmatEvent.__name__:
            return JSONSerializer._deserialize_drop_hazmat_event(payload)
        elif object_type == PickupHazmatEvent.__name__:
            return JSONSerializer._deserialize_pickup_hazmat_event(payload)
        elif object_type == OpenDoorEvent.__name__:
            return JSONSerializer._deserialize_open_door_event(payload)
        elif object_type == EndTurnAdvanceFireEvent.__name__:
            return JSONSerializer._deserialize_end_turn_advance_fire_event(payload)
        elif object_type == CloseDoorEvent.__name__:
            return JSONSerializer._deserialize_close_door_event(payload)
        elif object_type == SetInitialPOIFamilyEvent.__name__:
            return JSONSerializer._deserialize_set_initial_poi_family_event(payload)
        elif object_type == PlaceHazmatEvent.__name__:
            return JSONSerializer._deserialize_place_hazmat_event(payload)
        elif object_type == VehiclePlacedEvent.__name__:
            return JSONSerializer._deserialize_vehicle_placed_event(payload)
        elif object_type == DriveVehicleEvent.__name__:
            return JSONSerializer._deserialize_drive_vehicle_event(payload)
        elif object_type == IdentifyPOIEvent.__name__:
            return JSONSerializer._deserialize_identify_poi_event(payload)
        elif object_type == RideVehicleEvent.__name__:
            return JSONSerializer._deserialize_ride_vehicle_event(payload)
        elif object_type == DismountVehicleEvent.__name__:
            return JSONSerializer._deserialize_dismount_vehicle_event(payload)
        elif object_type == ChooseCharacterEvent.__name__:
            return JSONSerializer._deserialize_choose_character_event(payload)
        elif object_type == RemoveHazmatEvent.__name__:
            return JSONSerializer._deserialize_remove_hazmat_event(payload)
        elif object_type == ResuscitateEvent.__name__:
            return JSONSerializer._deserialize_resuscitate_event(payload)
        elif object_type == DodgeReplyEvent.__name__:
            return JSONSerializer._deserialize_dodge_reply(payload)
        elif object_type == RandomBoardSetupEvent.__name__:
            return JSONSerializer._deserialize_random_board_event(payload)
        elif object_type == BoardSetupEvent.__name__:
            return BoardSetupEvent(payload['seed'])
        elif object_type == NullModel.__name__:
            return NullModel()
        elif object_type == FireDeckGunEvent.__name__:
            return JSONSerializer._deserialize_fire_deck_gun_event(payload)

        logger.warning(f"Could not deserialize object {object_type}, not of recognized type.")

    @staticmethod
    def _safe_tile_serialize(tile: TileModel):
        return {
            'class': "TileModel",
            '_row': tile.row,
            '_column': tile.column,
            '_space_kind': {"name": type(SpaceKindEnum).__name__, "value": tile.space_kind.value},
            '_space_status': {"name": type(SpaceStatusEnum).__name__, "value": tile.space_status.value},
            '_is_hotspot': tile.is_hotspot,
            '_associated_models': [JSONSerializer.serialize(obj) for obj in tile.associated_models],
            '_visit_count': tile.visit_count,
            '_adjacent_edge_objects': JSONSerializer.serialize(tile.adjacent_edge_objects),
            '_arrow_dirn': {"name": type(ArrowDirectionEnum).__name__, "value": tile.arrow_dirn.value}
        }

    @staticmethod
    def _safe_dict(obj):

        if isinstance(obj, HazmatSprite):
            print("fuck")

        if isinstance(obj, Observer):
            return {"class": type(obj).__name__}

        if isinstance(obj, TileModel):
            return JSONSerializer._safe_tile_serialize(obj)

        obj.__setattr__("class", type(obj).__name__)
        return obj.__dict__ if not isinstance(obj, enum.Enum) else {"name": type(obj).__name__, "value": obj.value}

    @staticmethod
    def serialize(input_obj: object) -> dict:
        """Perform a deep serialize to a dict, then can be dumped into json file."""
        return json.loads(json.dumps(input_obj, default=lambda x: JSONSerializer._safe_dict(x)))
