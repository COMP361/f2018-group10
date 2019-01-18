

class WallModel(object):
    """Logical state of a Wall object."""

    def __init__(self):
        self._damage = 0
        self._broken = False
        self._adjacent_tiles = []
