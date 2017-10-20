from pathfinding import AStar
from grid import Grid

matrix = list(list(map(int, i)) for i in (
    '0000000000000000',
    '0111111100101010',
    '0100000000101010',
    '0101111111101010',
    '0101000000001010',
    '0101011111101010',
    '0101000000101010',
    '0001111100101110',
    '0101000000101010',
    '0101101011101010',
    '0101001010001000',
    '0101101010111010',
    '0101001010000010',
    '0101011111111010',
    '0101000100000010'))
grid = Grid(matrix=matrix)

start = grid.node(0, 14)
end = grid.node(8, 14)

path = AStar.find_path(start, end, grid)

print('path length:', len(path))
print(path)
print(grid.toStr(path=path, start=start, end=end))
