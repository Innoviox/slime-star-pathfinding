from pathfinding import AStar, file
import time

astar = AStar(*file.load_state_from_file('grid_save_2_21x21.txt'))
for path in astar.find_path_iter():
    print(path) 
 #   time.sleep(0.1)  
