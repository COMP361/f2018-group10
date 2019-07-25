import json
import random
from typing import List, Tuple, Dict


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

    def __init__(self, row: int, column: int, width: int, height: int, min_size: int, max_size: int):
        self._min_size = min_size
        self._max_size = max_size
        self.row = row
        self.column = column
        self.width = width
        self.height = height

        self.door_paths: List[Path] = []
        self.room = None
        self.left_child = None
        self.right_child = None

    def __str__(self):
        return f"Node: ({self.row}, {self.column}), {self.width}x{self.height}"

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

        max_split = self.height - self._min_size if split_horizontal else self.width - self._min_size
        if max_split <= self._min_size:
            return False

        split = random.randint(self._min_size, max_split)
        if split_horizontal:
            self.left_child = Node(self.row, self.column, self.width, split, self._min_size, self._max_size)
            self.right_child = Node(self.row + split, self.column, self.width, self.height - split, self._min_size, self._max_size)
        else:
            self.left_child = Node(self.row, self.column, split, self.height, self._min_size, self._max_size)
            self.right_child = Node(self.row, self.column + split, self.width - split, self.height, self._min_size, self._max_size)
        return True

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

        self.root = Node(1, 1, board_width, board_height, min_room_size, max_room_size)
        self.nodes = []
        self.leaves: List[Node] = []

        self._init_bsp()
        self._find_leaf_rooms(self.root)

    def _find_leaf_rooms(self, node: Node):
        """Initialize the list of all leaf nodes for convienience"""
        if node.left_child:
            self._find_leaf_rooms(node.left_child)
        if node.right_child:
            self._find_leaf_rooms(node.right_child)
        if not node.left_child and not node.right_child:
            #  We are at a leaf!
            self.leaves.append(node)

    def _init_bsp(self):
        self.nodes.append(self.root)
        did_split = True

        while did_split:
            did_split = False
            for node in self.nodes:
                if not node.left_child and not node.right_child:
                    if node.height > self.max_room_size or node.width > self.max_room_size:
                        if node.split():
                            self.nodes.append(node.left_child)
                            self.nodes.append(node.right_child)
                            did_split = True
        self.root.create_rooms()


class BoardGenerator(object):
    """Random Board generator, creates a JSON for how to place walls and doors."""

    def __init__(self, board_width: int, board_height: int, min_room_size: int, max_room_size:int):
        self.tree = BinarySpacePartition(board_width, board_height, min_room_size, max_room_size)
        self.board_width = board_width
        self.board_height = board_height

    def extract_all_paths(self) -> List[Path]:
        paths = []
        for leaf in self.tree.leaves:
            for path in leaf.door_paths:
                paths.append(path)
        return paths

    def intersect_path(self, leaves: List[Node], direction: str, line: List[Tuple]) -> List[Dict]:
        """Find out where along the straight path the doors should be placed. (Anywhere they intersect a room."""
        doors = []

        for spot in line:
            for leaf in leaves:
                room = leaf.room
                if direction == "North":
                    if spot[1] == room.top and room.left <= spot[0] <= room.right:
                        doors.append({
                            "first_pair": [spot[0], spot[1]-1],
                            "first_dirn": "South",
                            "obstacle_type": "door",
                            "second_pair": [spot[0], spot[1]],
                            "second_dirn": "North"
                        })
                elif direction == "East":
                    if spot[0] == room.right and room.top <= spot[1] <= room.bottom:
                        doors.append({
                            "first_pair": [spot[0], spot[1]],
                            "first_dirn": "East",
                            "obstacle_type": "door",
                            "second_pair": [spot[0]+1, spot[1]],
                            "second_dirn": "West"
                        })
                elif direction == "West":
                    if spot[0] == room.left and room.top <= spot[1] <= room.bottom:
                        doors.append({
                            "first_pair": [spot[0], spot[1]],
                            "first_dirn": "East",
                            "obstacle_type": "door",
                            "second_pair": [spot[0]-1, spot[1]],
                            "second_dirn": "West"
                        })
                elif direction == "South":
                    if spot[1] == room.bottom and room.left <= spot[0] <= room.right:
                        doors.append({
                            "first_pair": [spot[0], spot[1]],
                            "first_dirn": "South",
                            "obstacle_type": "door",
                            "second_pair": [spot[0], spot[1]+1],
                            "second_dirn": "North"
                        })
        return doors

    def create_walls_and_dumb_doors(self, leaf: Node) -> List[Dict]:
        """Create a rectangle of walls around this leaf node room."""
        walls_and_doors = []
        top_row = [(leaf.room.top, leaf.room.left + i) for i in range(leaf.room.width)]
        bottom_row = [(leaf.room.bottom, leaf.room.left + i) for i in range(leaf.room.width)]
        right_column = [(leaf.room.top + i, leaf.room.right) for i in range(leaf.room.height)]
        left_column = [(leaf.room.top + i, leaf.room.left) for i in range(leaf.room.height)]

        for spot in top_row:
            if leaf.room.top == 1:
                break

            walls_and_doors.append({
                "first_pair": [spot[0]-1, spot[1]],
                "first_dirn": "South",
                "obstacle_type": "wall",
                "second_pair": [spot[0], spot[1]],
                "second_dirn": "North"
            })

        for spot in bottom_row:
            if leaf.room.bottom == self.board_height:
                break

            walls_and_doors.append({
                "first_pair": [spot[0], spot[1]],
                "first_dirn": "South",
                "obstacle_type": "wall",
                "second_pair": [spot[0]+1, spot[1]],
                "second_dirn": "North"
            })

        for spot in left_column:
            if leaf.room.left == 1:
                break
            walls_and_doors.append({
                "first_pair": [spot[0], spot[1]-1],
                "first_dirn": "East",
                "obstacle_type": "wall",
                "second_pair": [spot[0], spot[1]],
                "second_dirn": "West"
            })

        for spot in right_column:
            if leaf.room.right == self.board_width:
                break
            walls_and_doors.append({
                "first_pair": [spot[0], spot[1]],
                "first_dirn": "East",
                "obstacle_type": "wall",
                "second_pair": [spot[0], spot[1]+1],
                "second_dirn": "West"
            })

        for i in random.sample(range(0, len(walls_and_doors)), 1):
            #  Choose a random wall and turn it into a door
            walls_and_doors[i]['obstacle_type'] = "door"
        return walls_and_doors

    def dict_equals(self, o1: Dict, o2: Dict):
        """Determine whether this door is in the same place as this wall"""
        return o1["first_pair"] == o2["first_pair"] and o1["second_pair"] == o2["second_pair"]

    def remove_dups(self, walls):
        seen_walls = []
        for wall in walls:
            has_been_seen = False
            for seen in seen_walls:
                if self.dict_equals(wall, seen):
                    has_been_seen = True
                    break

            if not has_been_seen:
                seen_walls.append(wall)
        return seen_walls

    def generate_inside_walls_doors(self):
        """
        Function for generating json files which contain information bout
        a randomly generated game board. These JSON can be used by the GameBoardModel to load
        the random board.
        """

        walls = []
        for leaf in self.tree.leaves:
            walls += self.create_walls_and_dumb_doors(leaf)

        walls = self.remove_dups(walls)

        with open("src/media/board_layouts/random_inside_walls_doors.json", mode="w", encoding='utf-8') as f:
            json.dump(walls, f)
