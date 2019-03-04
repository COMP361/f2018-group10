#############
# Directly run the script to see the result
############
import json

from src.constants.state_enums import SpaceKindEnum
from src.models.game_board.null_tile_model import NullTileModel
from src.models.game_board.tile_model import TileModel


# def main():
#     with open("../../media/board_layouts/tiles_adjacencies.json", "r") as f:
#         adj_dict = json.load(f)
#
#     for adj in adj_dict:
#         print(adj)

def test():
    tiles = []
    tiles.append([])
    tiles[0].append(TileModel(4, 3, SpaceKindEnum.INDOOR))
    tiles[0].append(TileModel(5, 1, SpaceKindEnum.OUTDOOR))
    tiles[0].append(TileModel(6, 7, SpaceKindEnum.INDOOR))
    tiles.append([])
    tiles[1].append(TileModel(3, 8, SpaceKindEnum.INDOOR))
    tiles[1].append(TileModel(3, 0, SpaceKindEnum.OUTDOOR))
    tiles[1].append(TileModel(6, 2, SpaceKindEnum.INDOOR))
    print("Original tiles:")
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            print(tiles[i][j], end='')
        print()
    print()

    extended_grid = []
    for row in tiles:
        extended_grid.append([give_test_tile()] + row + [give_test_tile()])

    row_length = len(tiles[0])
    extra_top_row = [give_test_tile() for x in range(row_length+2)]
    extra_bottom_row = [give_test_tile() for x in range(row_length+2)]
    extended_grid = [extra_top_row] + extended_grid + [extra_bottom_row]

    for i in range(1, len(extended_grid) - 1):
        for j in range(1, len(extended_grid[0]) - 1):
            extended_grid[i][j].north_tile = extended_grid[i - 1][j]
            extended_grid[i][j].east_tile = extended_grid[i][j + 1]
            extended_grid[i][j].west_tile = extended_grid[i][j - 1]
            extended_grid[i][j].south_tile = extended_grid[i + 1][j]

    print("After adding neighboring tiles:")
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            print("main tile", tiles[i][j])
            print("north tile", tiles[i][j].north_tile)
            print("east tile", tiles[i][j].east_tile)
            print("west tile", tiles[i][j].west_tile)
            print("south tile", tiles[i][j].south_tile)
            print()


def give_test_tile():
    return TileModel(-1, -1, SpaceKindEnum.INDOOR)


if __name__ == '__main__':
    test()