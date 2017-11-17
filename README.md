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


    |-- GitHub
        |-- __init__.py
        |-- test.py
        |-- view_test.py
        |-- pathfinding
        |   |-- __init__.py
        |   |-- core
        |   |   |-- __init__.py
        |   |   |-- finders.py
        |   |   |-- grid.py
        |   |   |-- heuristics.py
        |   |   |-- node.py
        |   |   |-- path.py
        |   |-- util
        |       |-- __init__.py
        |       |-- file.py
        |-- view
            |-- __init__.py
            |-- view.py



Todo:
 - add more utilities and addons
