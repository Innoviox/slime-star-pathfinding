# slime-star-pathfinding

A simple AStar visualizer in Python 3.

Simple text usage:

    from pathfinding import AStar, file

    astar = AStar(*file.load_state_from_file('grid_save_2_21x21.txt'))
    for path in astar.find_path_iter():
        print(path, end='')
        
Simple view usage:

    from pathfinding.util import file
    from view.view import GridView


    start, end, matrix = file.load_state_from_file('grid_save_2_21x21.txt')
    grid = GridView(matrix=matrix.matrix, start=start.position(), end=end.position())
    grid.mainloop()
    
Package structure:

/pathfinding
    /core
        finders
        grid
        heuristics
        node
        path
    /util
        file
/view
  view


Todo:
 - add more utilities and addons
