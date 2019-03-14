from src.action_events.end_game_event import EndGameEvent
from src.constants.state_enums import GameStateEnum
from src.core.networking import Networking
from src.models.game_state_model import GameStateModel
from src.observers.game_state_observer import GameStateObserver


class WinLoseController(GameStateObserver):

    def __init__(self):

        super().__init__()
        GameStateModel.instance().add_observer(self)





    def notify_player_index(self, player_index: int):
        pass

    def notify_game_state(self, game_state: GameStateEnum):
        print(game_state)
        if game_state in [GameStateEnum.LOST, GameStateEnum.WON]:
            event = EndGameEvent(game_state)
            try:
                Networking.get_instance().send_to_all_client(event)
            except AttributeError as e:
                pass


    def damage_changed(self, new_damage: int):
        pass

    def saved_victims(self, victims_saved: int):
        pass

    def dead_victims(self, victims_dead: int):
        pass


