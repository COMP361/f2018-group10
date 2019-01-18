from src.constants.enums.WallStatusEnum import WallStatusEnum


class WallModel(object):
    """Logical state of a Wall object."""

    def __init__(self):
        self._wall_status = WallStatusEnum.INTACT
        self._adjacent_tiles = []
