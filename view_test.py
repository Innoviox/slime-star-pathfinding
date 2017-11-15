from view.view import GridView
import file

matrix, start, end = file.load_state_from_file(21, 21)#5, 5, filename="grid_test")
print(start, end)
grid = GridView(matrix=matrix, start=start, end=end) #creates default 20x20 matrix
grid.mainloop()

#grid=GridView(matrix=None, dw=5, dh=5, filename="grid_test")
#grid.mainloop()
