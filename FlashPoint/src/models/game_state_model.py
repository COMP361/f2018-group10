import random
from threading import RLock

from typing import List, Optional, Tuple

from src.models.model import Model
from src.models.game_board.game_board_model import GameBoardModel
from src.constants.state_enums import GameKindEnum, DifficultyLevelEnum, GameStateEnum
from src.core.flashpoint_exceptions import TooManyPlayersException, InvalidGameKindException, PlayerNotFoundException
from src.models.game_units.player_model import PlayerModel


class GameStateModel(Model):
    """Singleton Class for maintaining the current Game state."""
    _instance = None
    lock = RLock()

    def __init__(self, host: PlayerModel, num_players: int, game_kind: GameKindEnum):
        print("Initializing game state...")

        with GameStateModel.lock:
            if not GameStateModel._instance:
                super().__init__()
                self._host = host
                self._max_desired_players = 6
                self._players = [self._host]
                self._players_turn_index = 0
                self._difficulty_level = None
                self._rules = game_kind
                self._red_dice = 0
                self._black_dice = 0

                self._victims_saved = 0
                self._victims_lost = 0
                self._damage = 0
                self._max_damage = 24
                self._chat_history = []
                self._state = GameStateEnum.READY_TO_JOIN

                self._game_board = GameBoardModel(self._rules)

                GameStateModel._instance = self
            else:
                print("Attempted to instantiate another singleton")
                raise Exception("GameStateModel is a Singleton")

    @staticmethod
    def __del__():
        with GameStateModel.lock:
            print("Lock acquired del")
            GameStateModel._instance = None
        print("Lock released del")

    @classmethod
    def instance(cls):
        """Get the instance of this singleton"""
        with GameStateModel.lock:
            print("Lock acquired instance")
            print("Lock released istance")
            return cls._instance

    @classmethod
    def set_game(cls, game):
        with GameStateModel.lock:

            print("Lock acquired set_game")
            cls._instance = game
        print("Lock released set game")

    @property
    def game_board(self) -> GameBoardModel:
        with GameStateModel.lock:
            print("Lock acquired game_board")
            print("Lock released game board")

            return self._game_board

    @property
    def chat_history(self) -> List[Tuple[str, str]]:
        with GameStateModel.lock:
            print("Lock acquired chat history")
            print("Lock released chat history")
            return self._chat_history

    def add_chat_message(self, message: str, sender_nickname: str):
        """Add a chat message to the history."""
        with GameStateModel.lock:
            print("lock acquired add chat message")
            self._chat_history.append((message, sender_nickname))
        print("Lock released add chat message")

    @property
    def host(self) -> PlayerModel:
        """Get the PlayerModel assigned to the host of the current game."""
        with GameStateModel.lock:
            print("Lock acquired host")
            return self._host

    @property
    def max_players(self) -> int:
        with GameStateModel.lock:
            print("Lock acquired max_players")
            return self._max_desired_players

    @max_players.setter
    def max_players(self, max_players: int):
        with GameStateModel.lock:
            print("Lock acquired max players set")
            self._max_desired_players = max_players
        print("Lock released max players set")


    @property
    def players(self)-> List[PlayerModel]:
        with GameStateModel.lock:
            print("Lock acquired players")
            return self._players

    def add_player(self, player: PlayerModel):
        """Add a player to the current game."""
        with GameStateModel.lock:
            print("Lock acquired add player")
            if len(self._players) == self._max_desired_players:
                raise TooManyPlayersException(player)
            self._players.append(player)
        print("Lock released add player")

    def get_player_by_ip(self, ip: str) -> PlayerModel:
        with GameStateModel.lock:
            print("Lock acquired get player by ip")
            matching_players = [player for player in self._players if player.ip == ip]
            if not matching_players:
                raise PlayerNotFoundException
            return matching_players[0]

    def remove_player(self, player: PlayerModel):
        """Remove a player from the current game."""
        with GameStateModel.lock:
            print("Lock acquired remove player")
            self._players.remove(player)
        print("Lock released remove player")

    @property
    def players_turn(self) -> PlayerModel:
        """The player who's turn it currently is."""
        with GameStateModel.lock:
            print("lock acqired players turn read")
            return self._players[self._players_turn_index]

    @players_turn.setter
    def players_turn(self, turn: int):
        with GameStateModel.lock:
            print("Lock acquired players turn set")
            self._players_turn_index = turn

    def next_player(self):
        """Rotate to the next player in the players list, round robin style."""
        with GameStateModel.lock:
            print("Lock acquired next player")
            self._players_turn_index = (self._players_turn_index + 1) % len(self._players)

    @property
    def difficulty_level(self) -> Optional[DifficultyLevelEnum]:
        """Difficulty level of an experienced game. A Family game should not have a difficulty level."""
        with GameStateModel.lock:
            print("Lock acquired difficulty level")
            if self._rules != GameKindEnum.FAMILY or None:
                print("WARNING: GameKind is FAMILY, you should not be accessing Difficulty Level.")
                return
            return self._difficulty_level

    @difficulty_level.setter
    def difficulty_level(self, level: DifficultyLevelEnum):
        """Set the difficulty level of the game. Game must be of type EXPERIENCED"""
        with GameStateModel.lock:
            print("Lock acquired difficulty lvl setter")
            if self._rules != GameKindEnum.EXPERIENCED or None:
                raise InvalidGameKindException("set difficulty level", self._rules)
            self._difficulty_level = level

    @property
    def rules(self) -> GameKindEnum:
        """The Game rules, one of GameKindEnum.FAMILY or GameKindEnum.EXPERIENCED"""
        with GameStateModel.lock:
            print("LOck aquired rules")
            return self._rules

    @rules.setter
    def rules(self, rules: GameKindEnum):
        """Set the rules for this game. one of GameKindEnum.FAMILY or GameKindEnum.EXPERIENCED"""
        with GameStateModel.lock:
            print("Lock acquired rules setter")
            self._rules = rules

    @property
    def roll_black_dice(self) -> int:
        """Roll the black dice to get a random number between 1-8"""
        return random.randint(1, 8)

    @property
    def roll_red_dice(self) -> int:
        """Roll the black dice to get a random number between 1-6"""
        return random.randint(1, 6)

    @property
    def victims_saved(self) -> int:
        with GameStateModel.lock:
            return self._victims_saved

    @victims_saved.setter
    def victims_saved(self, victims_saved: int):
        with GameStateModel.lock:
            self._victims_saved = victims_saved

    @property
    def victims_lost(self) -> int:
        with GameStateModel.lock:
            return self._victims_lost

    @victims_lost.setter
    def victims_lost(self, victims_lost: int):
        with GameStateModel.lock:
            self._victims_lost = victims_lost

    @property
    def damage(self) -> int:
        with GameStateModel.lock:
            return self._damage

    @damage.setter
    def damage(self, damage: int):
        with GameStateModel.lock:
            self._damage = damage

    @property
    def max_damage(self) -> int:
        with GameStateModel.lock:
            return self._max_damage

    @max_damage.setter
    def max_damage(self, damage: int):
        with GameStateModel.lock:
            self._max_damage = damage

    @property
    def state(self) -> GameStateEnum:
        with GameStateModel.lock:
            return self._state

    @state.setter
    def state(self, game_state: GameStateEnum):
        with GameStateModel.lock:
            self._state = game_state

    def game_lost(self):
        with GameStateModel.lock:
            self._state = GameStateEnum.LOST
