import enum
import json
from typing import Dict

from src.action_events.end_turn_advance_fire import EndTurnAdvanceFireEvent
from src.action_events.turn_events.chop_event import ChopEvent
from src.action_events.turn_events.close_door_event import CloseDoorEvent
from src.action_events.turn_events.drop_victim_event import DropVictimEvent
from src.action_events.turn_events.extinguish_event import ExtinguishEvent
from src.action_events.advance_fire_event import AdvanceFireEvent
from src.action_events.turn_events.move_event import MoveEvent
from src.action_events.turn_events.pick_up_victim_event import PickupVictimEvent
from src.action_events.turn_events.open_door_event import OpenDoorEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_board.wall_model import WallModel
from src.models.game_units.victim_model import VictimModel
from src.observers.observer import Observer
from src.models.game_board.tile_model import TileModel
from src.action_events.turn_events.choose_starting_position_event import ChooseStartingPositionEvent
from src.action_events.turn_events.end_turn_event import EndTurnEvent
from src.action_events.start_game_event import StartGameEvent
from src.action_events.ready_event import ReadyEvent
from src.action_events.chat_event import ChatEvent
from src.action_events.dummy_event import DummyEvent
from src.action_events.join_event import JoinEvent
from src.constants.state_enums import DifficultyLevelEnum, GameKindEnum, PlayerStatusEnum, WallStatusEnum, \
    DoorStatusEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class JSONSerializer(object):
    """Used for serializing and deserializing objects to JSON."""

    @staticmethod
    def _deserialize_game_state(payload: Dict) -> GameStateModel:
        """Deserialize a game state"""

        GameStateModel.lock.acquire()
        host: PlayerModel = JSONSerializer.deserialize(payload['_host'])
        num_players = payload['_max_desired_players']
        rules = GameKindEnum(payload['_rules']["value"])

        if not GameStateModel.instance():
            game = GameStateModel(host, num_players, rules)
        else:
            game = GameStateModel.instance()

        game.game_board.set_adjacencies(game.game_board.get_tiles())
        for player in [x for x in payload['_players'] if x['_ip'] != host.ip]:
            player_obj: PlayerModel = JSONSerializer.deserialize(player)
            if player_obj not in game.players:
                game.add_player(player_obj)

        if rules == GameKindEnum.EXPERIENCED:
            game.difficulty_level = DifficultyLevelEnum(payload['_difficulty_level']['value'])

        game.players_turn = payload['_players_turn_index']
        game.damage = payload['_damage']
        game.max_damage = payload['_max_damage']
        game.victims_lost = payload['_victims_lost']
        game.victims_saved = payload['_victims_saved']

        GameStateModel.lock.release()
        return game

    @staticmethod
    def _deserialize_player(payload: Dict) -> PlayerModel:
        ip = payload["_ip"]
        nickname = payload['_nickname']

        player = PlayerModel(ip, nickname)
        player.set_pos(payload['_row'], payload['_column'])
        player.color = tuple(payload['_color'])
        player.status = PlayerStatusEnum(payload["_status"]["value"])
        player.ap = payload['_ap']
        player.special_ap = payload['_special_ap']
        player.wins = payload['_wins']
        player.losses = payload['_losses']

        return player

    @staticmethod
    def _deserialize_victim(payload) -> VictimModel:
        victim_state = payload['_state']
        serialized_victim: VictimModel = VictimModel(victim_state)
        serialized_victim.set_pos(payload['_row'], payload['_column'])

        return serialized_victim

    @staticmethod
    def _deserialize_chat_event(payload: Dict) -> ChatEvent:
        message = payload['_message']
        sender = payload['_sender']
        return ChatEvent(message, sender)

    @staticmethod
    def _deserialize_ready_event(payload: Dict) -> ReadyEvent:
        player: PlayerModel = JSONSerializer.deserialize(payload['_player'])
        ready: bool = payload['_ready']
        return ReadyEvent(player, ready)

    @staticmethod
    def _deserialize_join_event(payload: Dict) -> JoinEvent:
        player = JSONSerializer._deserialize_player(payload['player'])
        return JoinEvent(player)

    @staticmethod
    def _deserialize_choose_position_event(payload: Dict):
        tile_dict = payload['tile']
        tile: TileModel = GameStateModel.instance().game_board.get_tile_at(tile_dict['_row'], tile_dict['_column'])
        GameStateModel.instance().game_board.set_single_tile_adjacencies(tile)
        event = ChooseStartingPositionEvent(tile)
        return event

    @staticmethod
    def _deserialize_move_event(payload: Dict):
        game_board = GameStateModel.instance().game_board
        destination = payload['destination']
        # dest_model = game_board.get_tile_at(destination['_row'], destination['_column'])
        tile_list = payload['moveable_tiles']
        moveable_tiles = []
        for tile in tile_list:
            tile_model: TileModel = game_board.get_tile_at(tile['_row'], tile['_column'])
            moveable_tiles.append(tile_model)

        destination_model: TileModel = game_board.get_tile_at(destination['_row'], destination['_column'])
        game_board.set_adjacencies(game_board.get_tiles())
        event = MoveEvent(destination_model, moveable_tiles)
        return event

    @staticmethod
    def _deserialize_tile(payload: Dict) -> TileModel:
        tile: TileModel = TileModel(payload['_row'], payload['_column'], payload['_space_kind'])
        GameStateModel.instance().game_board.set_single_tile_adjacencies(tile)
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
    def _deserialize_chop_event(payload: Dict) -> ChopEvent:
        wall: WallModel = JSONSerializer.deserialize(payload['wall'])
        return ChopEvent(wall)


    @staticmethod
    def _deserialize_extinguish_event(payload: Dict) -> ExtinguishEvent:

        tile_dict = payload['extinguish_space']
        tile: TileModel = GameStateModel.instance().game_board.get_tile_at(tile_dict['_row'], tile_dict['_column'])
        GameStateModel.instance().game_board.set_single_tile_adjacencies(tile)
        return ExtinguishEvent(tile)

    @staticmethod
    def _deserialize_end_turn_event(payload: Dict) -> EndTurnEvent:
        player: PlayerModel = JSONSerializer.deserialize(payload['player'])
        return EndTurnEvent(player)

    @staticmethod
    def _deserialize_open_door_event(payload: Dict) -> OpenDoorEvent:
        door: DoorModel = JSONSerializer.deserialize(payload['door'])
        return OpenDoorEvent(door)

    @staticmethod
    def _deserialize_close_door_event(payload: Dict) -> CloseDoorEvent:
        door: DoorModel = JSONSerializer.deserialize(payload['door'])
        return CloseDoorEvent(door)

    @staticmethod
    def _deserialize_advance_fire_event(payload: Dict) -> AdvanceFireEvent:
        red_dice: int = payload['red_dice']
        black_dice: int = payload['black_dice']
        event = AdvanceFireEvent(red_dice, black_dice)
        board = GameStateModel.instance().game_board
        board.set_adjacencies(board.get_tiles())
        return event

    @staticmethod
    def _deserialize_end_turn_advance_fire_event(payload: Dict) -> EndTurnAdvanceFireEvent:
        red_dice: int = payload['red_dice']
        black_dice: int = payload['black_dice']
        event = EndTurnAdvanceFireEvent(red_dice, black_dice)
        board = GameStateModel.instance().game_board
        board.set_adjacencies(board.get_tiles())
        return event

    @staticmethod
    def _deserialize_drop_event(payload: Dict) -> DropVictimEvent:
        victim: VictimModel = JSONSerializer.deserialize(payload['victim'])
        return DropVictimEvent(victim)


    @staticmethod
    def _deserialize_pickup_event(payload: Dict) -> PickupVictimEvent:
        victim: VictimModel = JSONSerializer.deserialize(payload['victim'])
        return PickupVictimEvent(victim)

    @staticmethod
    def deserialize(payload: Dict) -> object:
        """
        Grab an object and deserialize it.
        Note that the object must be able to take a dict as input. If there are nested objects or enums in the object,
        it must define its own _deserialize method by implementing the Serializable abstract class.

        Add to this case statement to be able to deserialize your object type.
        """
        object_type = payload["class"]
        if GameStateModel.instance():
            GameStateModel.instance().game_board.set_adjacencies(GameStateModel.instance().game_board.get_tiles())

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
        # --------------EVENTS------------------
        elif object_type == JoinEvent.__name__:
            return JSONSerializer._deserialize_join_event(payload)
        elif object_type == ChatEvent.__name__:
            return JSONSerializer._deserialize_chat_event(payload)
        elif object_type == ReadyEvent.__name__:
            return JSONSerializer._deserialize_ready_event(payload)
        elif object_type == StartGameEvent.__name__:
            return StartGameEvent()
        elif object_type == EndTurnEvent.__name__:
            return JSONSerializer._deserialize_end_turn_event(payload)
        elif object_type == AdvanceFireEvent.__name__:
            return JSONSerializer._deserialize_advance_fire_event(payload)
        elif object_type == ChooseStartingPositionEvent.__name__:
            return JSONSerializer._deserialize_choose_position_event(payload)
        elif object_type == ChopEvent.__name__:
            return JSONSerializer._deserialize_chop_event(payload)
        elif object_type == MoveEvent.__name__:
            return JSONSerializer._deserialize_move_event(payload)
        elif object_type == DummyEvent.__name__:
            return DummyEvent()
        elif object_type == ExtinguishEvent.__name__:
            return JSONSerializer._deserialize_extinguish_event(payload)
        elif object_type == OpenDoorEvent.__name__:
            return JSONSerializer._deserialize_open_door_event(payload)
        elif object_type == EndTurnAdvanceFireEvent.__name__:
            return JSONSerializer._deserialize_end_turn_advance_fire_event(payload)
        elif object_type == CloseDoorEvent.__name__:
            return JSONSerializer._deserialize_close_door_event(payload)
        elif object_type == DropVictimEvent.__name__:
            return JSONSerializer._deserialize_drop_event(payload)
        elif object_type == PickupVictimEvent.__name__:
            return JSONSerializer._deserialize_pickup_event(payload)

        print(f"WARNING: Could not deserialize object {object_type}, not of recognized type.")

    @staticmethod
    def _safe_dict(obj):

        if isinstance(obj, Observer):
            return {"class": type(obj).__name__}

        if isinstance(obj, TileModel):
            obj.reset_adjacencies()

        obj.__setattr__("class", type(obj).__name__)
        return obj.__dict__ if not isinstance(obj, enum.Enum) else {"name": type(obj).__name__, "value": obj.value}

    @staticmethod
    def serialize(input_obj: object) -> dict:
        """Perform a deep serialize to a dict, then can be dumped into json file."""
        return json.loads(json.dumps(input_obj, default=lambda x: JSONSerializer._safe_dict(x)))

