from pathfinding import AStar, file

astar = AStar(*file.load_state_from_file('grid_save_2_21x21.txt'))
for path in astar.find_path_iter():
    print(path, end='')
