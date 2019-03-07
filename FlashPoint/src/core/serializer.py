import enum
import json
from typing import Dict

from src.observers.observer import Observer
from src.models.game_board.tile_model import TileModel
from src.action_events.turn_events.choose_starting_position_event import ChooseStartingPositionEvent
from src.models.game_board.game_board_model import GameBoardModel
from src.action_events.start_game_event import StartGameEvent
from src.action_events.ready_event import ReadyEvent
from src.action_events.chat_event import ChatEvent
from src.action_events.dummy_event import DummyEvent
from src.action_events.join_event import JoinEvent
from src.constants.state_enums import DifficultyLevelEnum, GameKindEnum, PlayerStatusEnum
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
        player.set_pos(payload['_x_pos'], payload['_y_pos'])
        player.color = tuple(payload['_color'])
        player.status = PlayerStatusEnum(payload["_status"]["value"])
        player.ap = payload['_ap']
        player.special_ap = payload['_special_ap']
        player.wins = payload['_wins']
        player.losses = payload['_losses']

        return player

    @staticmethod
    def _deserialize_chat_event(payload: Dict) -> ChatEvent:
        message = payload['_message']
        sender = payload['_sender']
        return ChatEvent(message, sender)

    @staticmethod
    def _deserialize_ready_event(payload: Dict) -> ReadyEvent:
        player: PlayerModel = JSONSerializer.deserialize(payload['_player'])
        return ReadyEvent(player)

    @staticmethod
    def _deserialize_join_event(payload: Dict) -> JoinEvent:
        player = JSONSerializer._deserialize_player(payload['player'])
        return JoinEvent(player)

    @staticmethod
    def _deserialize_choose_position_event(payload: Dict):
        tile: TileModel = JSONSerializer.deserialize(payload['tile'])
        event = ChooseStartingPositionEvent(tile)
        event.player = JSONSerializer.deserialize(payload['player'])
        return event

    @staticmethod
    def deserialize(payload: Dict) -> object:
        """
        Grab an object and deserialize it.
        Note that the object must be able to take a dict as input. If there are nested objects or enums in the object,
        it must define its own _deserialize method by implementing the Serializable abstract class.

        Add to this case statement to be able to deserialize your object type.
        """
        object_type = payload["class"]
        if object_type == PlayerModel.__name__:
            return JSONSerializer._deserialize_player(payload)
        elif object_type == GameStateModel.__name__:
            return JSONSerializer._deserialize_game_state(payload)
        elif object_type == JoinEvent.__name__:
            return JSONSerializer._deserialize_join_event(payload)
        elif object_type == ChatEvent.__name__:
            return JSONSerializer._deserialize_chat_event(payload)
        elif object_type == ReadyEvent.__name__:
            return JSONSerializer._deserialize_ready_event(payload)
        elif object_type == StartGameEvent.__name__:
            return StartGameEvent()
        elif object_type == ChooseStartingPositionEvent.__name__:
            return JSONSerializer._deserialize_choose_position_event(payload)
        elif object_type == DummyEvent.__name__:
            return DummyEvent()

        print("WARNING: Could not deserialize object, not of recognized type.")

    @staticmethod
    def _safe_dict(obj):
        print(obj)
        if isinstance(obj, Observer):
            print("Observer, skipping serialize")
            return ""

        if isinstance(obj, TileModel):
            obj.reset_adjacencies()

        obj.__setattr__("class", type(obj).__name__)
        return obj.__dict__ if not isinstance(obj, enum.Enum) else {"name": type(obj).__name__, "value": obj.value}

    @staticmethod
    def serialize(input_obj: object) -> dict:
        """Perform a deep serialize to a dict, then can be dumped into json file."""
        return json.loads(json.dumps(input_obj, default=lambda x: JSONSerializer._safe_dict(x)))

