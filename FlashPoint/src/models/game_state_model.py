

class GameStateModel(object):
    """Class for maintaing the current Game state."""

    def __init__(self):
        self._seconds_since_start = 0
        self._players = []   # Might be dict of {ip : PlayerModel} but not sure yet
        self._current_player_turn = None  # Will be a PlayerModel object
        self._difficulty_level = None  # Some gametype enum
        self._rules = None  # Game mode
        self._red_dice = 0  # Some random number genetator between 1 and 6
        self._black_dice = 0  # Some random number generator between 1 and 8



