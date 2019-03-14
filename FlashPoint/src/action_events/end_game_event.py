import json

from src.action_events.action_event import ActionEvent
from src.constants.change_scene_enum import ChangeSceneEnum
from src.constants.state_enums import GameStateEnum, PlayerStatusEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue

from src.models.game_state_model import GameStateModel


class EndGameEvent(ActionEvent):
    """Event to signal every client that the game has finished"""

    def __init__(self, state:GameStateEnum):
        super().__init__()
        self._state = state



    def execute(self, *args, **kwargs):

        state_model = GameStateModel.instance()
        players = state_model.players
        profiles = "media/profiles.json"

        if self._state == GameStateEnum.LOST:
            for player in players:

                with open(profiles, mode='r+', encoding='utf-8') as file:
                    temp = json.load(file)
                    file.seek(0)
                    file.truncate()
                    for user in temp:
                        if user['_nickname'] == player.nickname:
                            losses = user['_losses']
                            user['_losses'] = losses + 1
                    json.dump(temp,file)
                player.status = PlayerStatusEnum.NOT_READY

            EventQueue.block()

            EventQueue.post(CustomEvent(ChangeSceneEnum.LOSESCENE))

        else:
            for player in players:

                with open(profiles, mode='r+', encoding='utf-8') as file:
                    temp = json.load(file)
                    file.seek(0)
                    file.truncate()
                    for user in temp:
                        if user['_nickname'] == player.nickname:
                            wins = user['_wins']
                            user['_wins'] = wins + 1
                    json.dump(temp,file)
                player.status = PlayerStatusEnum.NOT_READY

            EventQueue.block()
            EventQueue.post(CustomEvent(ChangeSceneEnum.WINSCENE))





