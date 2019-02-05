import enum
import json
from typing import Dict

from constants.state_enums import DifficultyLevelEnum, GameKindEnum, PlayerStatusEnum
from models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class JSONSerializer(object):
    """Used for serializing and deserializing objects to JSON."""

    @staticmethod
    def _deserialize_game_state(payload: Dict) -> GameStateModel:
        """Deserialize a game state"""
        host: PlayerModel = JSONSerializer.deserialize(payload['_host'])
        num_players = payload['_max_desired_players']
        rules = GameKindEnum(payload['_rules']["value"])
        game = GameStateModel(host, num_players, rules)

        for player in payload['_players']:
            player_obj: PlayerModel = JSONSerializer.deserialize(player)
            game.add_player(player_obj)

        if rules == GameKindEnum.EXPERIENCED:
            game.difficulty_level = DifficultyLevelEnum(payload['_difficulty_level']['value'])

        game.players_turn = payload['_players_turn_index']
        game.damage = payload['_damage']
        game.max_damage = payload['_max_damage']
        game.victims_lost = payload['_victims_lost']
        game.victims_saved = payload['_victims_saved']

        return game

    @staticmethod
    def _deserialize_player(payload: Dict) -> PlayerModel:
        ip = payload["_ip"]
        nickname = payload['_nickname']

        player = PlayerModel(ip, nickname)
        player.x_pos = payload['_x_pos']
        player.y_pos = payload['_y_pos']
        player.color = tuple(payload['_color'])
        player.status = PlayerStatusEnum(payload["_status"]["value"])
        player.ap = payload['_ap']
        player.special_ap = payload['_special_ap']
        player.wins = payload['_wins']
        player.losses = payload['_losses']

        return player

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

        print("WARNING: Could not deserialize object, not of recognized type.")

    @staticmethod
    def _safe_dict(obj):
        obj.__setattr__("class", type(obj).__name__)
        return obj.__dict__ if not isinstance(obj, enum.Enum) else {"name": type(obj).__name__, "value": obj.value}

    @staticmethod
    def serialize(input_obj: object) -> dict:
        """Perform a deep serialize to a dict, then can be dumped into json file."""
        return json.loads(json.dumps(input_obj, default=lambda x: JSONSerializer._safe_dict(x)))
