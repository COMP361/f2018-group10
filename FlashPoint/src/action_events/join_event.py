import src.constants.color as Color
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel


class JoinEvent(ActionEvent):
    def __init__(self, player: PlayerModel):
        super().__init__()
        self.player = player

    def execute(self):
        self.player.color = None

        colors = {
            "blue": Color.BLUE,
            "red": Color.RED,
            "orange": Color.ORANGE,
            "yellow": Color.YELLOW,
            "green": Color.GREEN,
            "white": Color.WHITE,
        }

        list_players = GameStateModel.instance().players

        for color in colors:
            color_available = True
            for player in list_players:
                if player.color == colors[color]:
                    color_available = False
                    break
                else:
                    continue
            if color_available:
                self.player.color = colors[color]
                break

        GameStateModel.instance().add_player(self.player)
