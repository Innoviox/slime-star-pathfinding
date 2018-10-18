from pathfinding import AStar, file

astar = AStar(*file.load_state_from_file('grid_test_9x9.ssp'))
for path in astar.find_path_iter():
    print(path, end='')
