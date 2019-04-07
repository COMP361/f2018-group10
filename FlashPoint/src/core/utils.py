import random
from typing import List, Tuple, Optional, Dict


class Room(object):
    def __init__(self, row: int, column: int, width: int, height: int):
        self.row = row
        self.column = column
        self.width = width
        self.height = height

    @property
    def as_tuple(self):
        return self.row, self.column, self.width, self.height

    @property
    def left(self):
        return self.column

    @property
    def right(self):
        return self.column + self.width - 1

    @property
    def top(self):
        return self.row

    @property
    def bottom(self):
        return self.row + self.height - 1

class Path(object):

    def __init__(self, direction: str, points: List[Tuple]):
        self.path = (direction, points)


class Node(object):
    """Representing a leaf of th Binary Space Partition Tree"""

    def __init__(self, row: int, column: int, width: int, height: int, min_size: int):
        self._min_size = min_size
        self.row = row
        self.column = column
        self.width = width
        self.height = height

        self.door_paths: List[Path] = []
        self.room = None
        self.left_child = None
        self.right_child = None

    def split(self) -> bool:
        """Split this leaf into two children"""
        if self.left_child or self.right_child:
            return False  # Already split this leaf!

        # Determine the direction of the split
        # If the width is >25% larger than height, split vertically
        # Otherwise split horizontally
        # If neither condition is true, randomly choose
        split_horizontal = random.random() > 0.5
        if self.width > self.height and self.width/self.height >= 1.25:
            split_horizontal = False
        elif self.height > self.width and self.height / self.width >= 1.25:
            split_horizontal = True

        max_v = self.height - self._min_size if split_horizontal else self.width - self._min_size
        if max_v <= self._min_size:
            return False  # Area is too small to split anymore

        split: int = random.randint(self._min_size, max_v)

        #  create left and right children
        if split_horizontal:
            self.left_child = Node(self.row, self.column, self.width, split, self._min_size)
            self.right_child = Node(self.row + split, self.column, self.width, self.height - split, self._min_size)
        else:
            self.left_child = Node(self.row, self.column, self.width, split, self._min_size)
            self.right_child = Node(self.row, self.column + split, self.width - split, self.height, self._min_size)

        return True  # Split successful!

    def get_room(self):
        if self.room:
            return self.room
        else:
            l_room = None
            r_room = None

            if self.left_child:
                l_room = self.left_child.get_room()
            if self.right_child:
                r_room = self.right_child.get_room()

            if not l_room and not r_room:
                return None
            elif not l_room:
                return r_room
            elif not r_room:
                return l_room
            elif random.random() > 0.5:
                return l_room
            else:
                return r_room

    def create_rooms(self):
        """Set the doors between the children of this leaf"""
        if self.left_child or self.right_child:
            if self.left_child:
                self.left_child.create_rooms()
            if self.right_child:
                self.right_child.create_rooms()

            if self.left_child and self.right_child:
                self.create_paths(self.left_child.get_room(), self.right_child.get_room())
        else:
            self.room = Room(self.row, self.column, self.width, self.height)

    def make_straight_path_between_points(self, direction: str, p1: Tuple, p2: Tuple) -> Path:
        """Must share common x or y coord"""
        path = []
        y_diff = p1[1] - p2[1]
        x_diff = p1[0] - p2[0]

        if direction == "North":
            i = 0
            while i <= y_diff:
                path.append((p1[0], p1[1] - i))
                i += 1

        elif direction == "West":
            i = 0
            while i <= x_diff:
                path.append((p1[0] - i, p1[1]))
                i += 1

        elif direction == "South":
            i = 0
            while i <= y_diff:
                path.append((p1[0], p1[1] + i))
                i += 1

        elif direction == "East":
            i = 0
            while i <= x_diff:
                path.append((p1[0] + i, p1[1]))
                i += 1

        return Path(direction, path)

    def create_paths(self, l_room, r_room):

        # Generate random points in each room
        l_room_point = (random.randint(l_room.left, l_room.right + 1), random.randint(l_room.top, l_room.bottom + 1))
        r_room_point = (random.randint(r_room.left, r_room.right + 1), random.randint(r_room.top, r_room.bottom + 1))

        x_diff = l_room_point[0] - r_room_point[0]
        y_diff = l_room_point[1] - r_room_point[1]

        vert_dir = ""
        hor_dir = ""

        if x_diff < 0:
            hor_dir = "West"
        elif x_diff > 0:
            hor_dir = "East"

        if y_diff < 0:
            vert_dir = "South"
        elif y_diff > 0:
            vert_dir = "North"

        hor_path = self.make_straight_path_between_points(hor_dir, l_room_point, r_room_point)
        vert_path = self.make_straight_path_between_points(vert_dir, l_room_point, r_room_point)

        #  Randomly add first horizontal then vertical or visa versa.
        if random.random() > 0.5:
            self.door_paths.append(vert_path)
            self.door_paths.append(hor_path)
        else:
            self.door_paths.append(hor_path)
            self.door_paths.append(vert_path)


class BinarySpacePartition(object):
    """Represents the rooms"""

    def __init__(self, board_width, board_height, min_room_size, max_room_size):
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size

        self.root = Node(0, 0, board_width, board_height, min_room_size)
        self.leaves = []

    def _init_bsp(self):
        self.leaves.append(self.root)
        did_split = True

        while did_split:
            for l in self.leaves:
                if not l.left_child and not l.right_child:
                    if l.width > self.max_room_size or l.height > self.max_room_size:
                        if l.split():
                            self.leaves.append(l.left_child)
                            self.leaves.append(l.right_child)
                            did_split = True


class BoardGenerator(object):
    """Random Board generator, creates a JSON for how to place walls and doors."""

    def __init__(self, board_width: int, board_height: int, min_room_size: int, max_room_size:int):
        self.tree = BinarySpacePartition(board_width, board_height, min_room_size, max_room_size)
        self.json = []

    def intersect_path(self, room: Room, direction: str, line: List[Tuple]) -> Optional[Dict]:
        """Find out where along the straight path the doors should be placed."""
        for spot in line:
            if direction == "North":
                if spot == room.top:
                    return {
                        
                    }
            elif direction == "East":
                pass
            elif direction == "West":
                pass
            elif direction == "South":
                pass

    def generate(self):
        """
        Function for generating json files which contain information bout
        a randomly generated game board. These JSON can be used by the GameBoardModel to load
        the random board.
        """


