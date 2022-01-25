from pathfinding.util import file
from view.view import GridView


# start, end, matrix = file.load_state_from_file('example_saves/grid_test_9x9.ssp')  #5, 5, filename="grid_test")
# grid = GridView(matrix=matrix.matrix, start=start.position(), end=end.position(), animated=True) #creates default 20x20 matrix
grid = GridView(animated=True)
grid.mainloop()

# grid=GridView(matrix=None, dw=50, dh=30, filename="grid_test")
# grid.mainloop()
