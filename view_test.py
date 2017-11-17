from pathfinding.util import file
from view.view import GridView


start, end, matrix = file.load_state_from_file('grid_save_2_21x21.txt')#5, 5, filename="grid_test")
grid = GridView(matrix=matrix.matrix, start=start.position(), end=end.position()) #creates default 20x20 matrix
grid.mainloop()

#grid=GridView(matrix=None, dw=5, dh=5, filename="grid_test")
#grid.mainloop()
