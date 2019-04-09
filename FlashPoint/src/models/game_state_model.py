import json
import os
import random
import logging
from threading import RLock

from typing import List, Optional, Tuple

from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.model import Model
from src.models.game_board.game_board_model import GameBoardModel
from src.constants.state_enums import GameKindEnum, DifficultyLevelEnum, GameStateEnum, VehicleOrientationEnum, \
    GameBoardTypeEnum, PlayerStatusEnum, PlayerRoleEnum
from src.core.flashpoint_exceptions import TooManyPlayersException, InvalidGameKindException, PlayerNotFoundException
from src.models.game_units.player_model import PlayerModel

logger = logging.getLogger("FlashPoint")


class GameStateModel(Model):
    """Singleton Class for maintaining the current Game state."""
    _instance = None
    lock = RLock()

    def __init__(self,
                 host: PlayerModel,
                 num_players: int,
                 game_kind: GameKindEnum,
                 board_type: GameBoardTypeEnum,
                 difficulty: DifficultyLevelEnum = None
                 ):

        if not GameStateModel._instance:
            logger.info("Initializing game state...")
            super().__init__()
            self._host = host
            self._max_desired_players = num_players
            self._players = [self._host]
            self._players_turn_index = 0
            self._difficulty_level = difficulty
            self._rules = game_kind

            self._board_type = board_type

            self._game_board = GameBoardModel(self._board_type)

            self._victims_saved = 0
            self._victims_lost = 0
            self._damage = 0
            self._max_damage = 24
            self._chat_history = []
            self._dodge_reply = False
            self._command = (None, None)
            self._commanded: List[PlayerModel] = []
            self._state = GameStateEnum.READY_TO_JOIN
            GameStateModel._instance = self
        else:
            raise Exception("GameStateModel is a Singleton")

    # def notify_all_observers(self):
    #     self._notify_state()
    #     self._game_board.notify_all_observers()

    def _notify_player_added(self, player: PlayerModel):
        for obs in self._observers:
            obs.player_added(player)

    def _notify_player_removed(self, player: PlayerModel):
        for obs in self._observers:
            obs.player_removed(player)

    def _notify_player_index(self):
        for obs in self._observers:
            obs.notify_player_index(self._players_turn_index)

    def _notify_state(self):
        for obs in self._observers:
            obs.notify_game_state(self._state)

    def _notify_command(self):
        for obs in self._observers:
            obs.player_command(self.command[0], self.command[1])

    @staticmethod
    def destroy():
        GameStateModel._instance = None
        logger.info("GameStateModel deleted")
        if os.path.exists("media/board_layouts/random_inside_walls.json"):
            os.rmdir("media/board_layouts/random_inside_walls.json")

    @classmethod
    def instance(cls):
        """Get the instance of this singleton"""
        return cls._instance

    @classmethod
    def set_game(cls, game):
        cls._instance = game

    @property
    def game_board(self) -> GameBoardModel:
        with GameStateModel.lock:
            return self._game_board

    @game_board.setter
    def game_board(self, board: GameBoardModel):
        with GameStateModel.lock:
            self._game_board = board

    @property
    def dodge_reply(self) -> bool:
        return self._dodge_reply

    @dodge_reply.setter
    def dodge_reply(self, reply: bool):
        self._dodge_reply = reply

    @property
    def command(self) -> Tuple[PlayerModel, PlayerModel]:
        if self._command[0] and self._command[1]:
            source = [player for player in self.players if player == self._command[0]][0]
            target = [player for player in self.players if player == self._command[1]][0]
            return source, target
        return None, None

    @command.setter
    def command(self, command: Tuple[PlayerModel, PlayerModel]):
        self._command = command
        if command[1].role is PlayerRoleEnum.CAFS:
            self._commanded.append(command[1])
        self._notify_command()

    @property
    def commanded_list(self):
        return self._commanded

    def clear_commanded_list(self):
        self._commanded.clear()

    @property
    def board_type(self) -> GameBoardTypeEnum:
        with GameStateModel.lock:
            return self._board_type

    @board_type.setter
    def board_type(self, board_type: GameBoardTypeEnum):
        with GameStateModel.lock:
            self._board_type = board_type
            if not self.game_board.is_loaded:
                self._game_board = GameBoardModel(board_type)

    @property
    def chat_history(self) -> List[Tuple[str, str]]:
        with GameStateModel.lock:
            return self._chat_history

    def add_chat_message(self, message: str, sender_nickname: str):
        """Add a chat message to the history."""
        with GameStateModel.lock:
            self._chat_history.append((message, sender_nickname))

    @property
    def host(self) -> PlayerModel:
        """Get the PlayerModel assigned to the host of the current game."""
        with GameStateModel.lock:
            return self._host

    @host.setter
    def host(self, host: PlayerModel):
        with GameStateModel.lock:
            self._host = host

    @property
    def max_players(self) -> int:
        with GameStateModel.lock:
            return self._max_desired_players

    @max_players.setter
    def max_players(self, max_players: int):
        with GameStateModel.lock:
            self._max_desired_players = max_players

    @property
    def players(self)-> List[PlayerModel]:
        with GameStateModel.lock:
            return self._players

    @players.setter
    def players(self, players: List[PlayerModel]):
        with GameStateModel.lock:
            self._players = players

    def add_player(self, player: PlayerModel):
        """Add a player to the current game."""
        with GameStateModel.lock:
            if len(self._players) == self._max_desired_players:
                raise TooManyPlayersException(player)
            self._players.append(player)
            self._notify_player_added(player)

    def get_player_by_ip(self, ip: str) -> PlayerModel:
        with GameStateModel.lock:
            matching_players = [player for player in self._players if player.ip == ip]
            if not matching_players:
                raise PlayerNotFoundException
            return matching_players[0]

    def remove_player(self, player: PlayerModel):
        """Remove a player from the current game."""
        with GameStateModel.lock:
            self._players.remove(player)
            self._notify_player_index()
            self._notify_player_removed(player)

    @property
    def players_turn_index(self) -> int:
        with GameStateModel.lock:
            return self._players_turn_index

    @property
    def players_turn(self) -> PlayerModel:
        """The player who's turn it currently is."""
        with GameStateModel.lock:
            return self._players[self._players_turn_index]

    @players_turn.setter
    def players_turn(self, turn: int):
        with GameStateModel.lock:
            self._players_turn_index = turn
            self._notify_player_index()

    def next_player(self):
        """Rotate to the next player in the players list, round robin style."""
        with GameStateModel.lock:
            self._players_turn_index = (self._players_turn_index + 1) % len(self._players)
            self._notify_player_index()

    @property
    def difficulty_level(self) -> Optional[DifficultyLevelEnum]:
        """Difficulty level of an experienced game. A Family game should not have a difficulty level."""
        with GameStateModel.lock:
            if self._rules == GameKindEnum.FAMILY or None:
                logger.warning("GameKind is FAMILY, you should not be accessing Difficulty Level.")
                return
            return self._difficulty_level

    @difficulty_level.setter
    def difficulty_level(self, level: DifficultyLevelEnum):
        """Set the difficulty level of the game. Game must be of type EXPERIENCED"""
        with GameStateModel.lock:
            if self._rules != GameKindEnum.EXPERIENCED or None:
                raise InvalidGameKindException("set difficulty level", self._rules)
            self._difficulty_level = level
            logger.info("Game difficulty level: {lvl}".format(lvl=level))

    @property
    def rules(self) -> GameKindEnum:
        """The Game rules, one of GameKindEnum.FAMILY or GameKindEnum.EXPERIENCED"""
        with GameStateModel.lock:
            return self._rules

    @rules.setter
    def rules(self, rules: GameKindEnum):
        """Set the rules for this game. one of GameKindEnum.FAMILY or GameKindEnum.EXPERIENCED"""
        with GameStateModel.lock:
            self._rules = rules
            logger.info("Game rules: {r}".format(r=rules))

    def roll_black_dice(self) -> int:
        """Roll the black dice to get a random number between 1-8"""
        with GameStateModel.lock:
            return random.randint(1, 8)

    def roll_red_dice(self) -> int:
        """Roll the red dice to get a random number between 1-6"""
        with GameStateModel.lock:
            return random.randint(1, 6)

    @property
    def victims_saved(self) -> int:
        with GameStateModel.lock:
            return self._victims_saved

    @victims_saved.setter
    def victims_saved(self, victims_saved: int):
        with GameStateModel.lock:
            self._victims_saved = victims_saved
            logger.info("Game victims saved: {vs}".format(vs=victims_saved))
            for obs in self._observers:
                obs.saved_victims(victims_saved)
            if self._victims_saved >= 7:
                self._state = GameStateEnum.WON
                self.endgame()

    @property
    def victims_lost(self) -> int:
        with GameStateModel.lock:
            return self._victims_lost

    @victims_lost.setter
    def victims_lost(self, victims_lost: int):
        with GameStateModel.lock:
            self._victims_lost = victims_lost
            logger.info("Game victims lost: {vl}".format(vl=victims_lost))
            for obs in self._observers:
                obs.dead_victims(victims_lost)
            if self._victims_lost >= 4:
                self._state = GameStateEnum.LOST
                self.endgame()

    @property
    def damage(self) -> int:
        with GameStateModel.lock:
            return self._damage

    @damage.setter
    def damage(self, damage: int):
        with GameStateModel.lock:
            self._damage = damage
            logger.info("Game damage: {d}".format(d=damage))
            for obs in self._observers:
                obs.damage_changed(damage)
            if self._damage >= self.max_damage:
                self._state = GameStateEnum.LOST
                self.endgame()

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
            logger.info("Game state: {s}".format(s=game_state))
            self._notify_state()
            if self._state == GameStateEnum.LOST:
                # TODO: More stuff here for what is supposed to happen when the game is lost.
                pass
            elif self._state == GameStateEnum.WON:
                # TODO: More stuff here for what is supposed to happen when the game is won.
                pass

    def game_lost(self):
        with GameStateModel.lock:
            self._state = GameStateEnum.LOST

    def get_players_on_tile(self, row: int, column) -> List[PlayerModel]:
        """
        Returns a list containing the players
        located on a given tile.

        :param row: target tile's row
        :param column: target tile's column
        :return: A list containing all the players on
                a given tile
        """
        with GameStateModel.lock:
            players_on_tile = []
            tile = self.game_board.get_tile_at(row, column)
            for player in self.players:
                if player.row == tile.row and player.column == tile.column:
                    players_on_tile.append(player)

            return players_on_tile

    def all_players_have_chosen_location(self) -> bool:
        """If all player locations are positive, then we know that they have chosen their position."""
        return all([player.column >= 0 and player.row >= 0 for player in self.players])

    def vehicles_have_been_placed(self) -> bool:
        ambulance_placed = self.game_board.ambulance.orientation != VehicleOrientationEnum.UNSET
        engine_placed = self.game_board.engine.orientation != VehicleOrientationEnum.UNSET
        return ambulance_placed and engine_placed

    def determine_black_dice_opposite_face(self, prev_roll: int) -> int:
        """
        Gives the opposite face on the black dice
        for the number prev_roll. (Based on the Koplow d8 -
        https://boardgamegeek.com/article/27926069#27926069)

        :param prev_roll: Number that the black dice rolled previously.
        :return: Number opposite to the previous roll.
        """
        if prev_roll == 1:
            return 6
        elif prev_roll == 2:
            return 5
        elif prev_roll == 3:
            return 8
        elif prev_roll == 4:
            return 7
        elif prev_roll == 5:
            return 2
        elif prev_roll == 6:
            return 1
        elif prev_roll == 7:
            return 4
        elif prev_roll == 8:
            return 3

    def endgame(self):

        profiles = "media/profiles.json"

        if self._state == GameStateEnum.LOST:
            for player in self.players:

                with open(profiles, mode='r+', encoding='utf-8') as file:
                    temp = json.load(file)
                    file.seek(0)
                    file.truncate()
                    for user in temp:
                        if user['_nickname'] == player.nickname:
                            losses = user['_losses']
                            user['_losses'] = losses + 1
                    json.dump(temp, file)
                player.status = PlayerStatusEnum.NOT_READY

            EventQueue.block()

            EventQueue.post(CustomEvent(ChangeSceneEnum.LOSESCENE))

        else:
            for player in self.players:

                with open(profiles, mode='r+', encoding='utf-8') as file:
                    temp = json.load(file)
                    file.seek(0)
                    file.truncate()
                    for user in temp:
                        if user['_nickname'] == player.nickname:
                            wins = user['_wins']
                            user['_wins'] = wins + 1
                    json.dump(temp, file)
                player.status = PlayerStatusEnum.NOT_READY

            EventQueue.block()
            EventQueue.post(CustomEvent(ChangeSceneEnum.WINSCENE))