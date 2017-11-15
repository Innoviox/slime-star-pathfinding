import numpy as np
def save_state_to_file(gridview, filename="grid_save", fileform="{}_{}x{}.ssp"):
    f = open(fileform.format(filename, gridview.gridFrame.w, gridview.gridFrame.h), "w")
    gf = gridview.gridFrame
    grid = gridview.gridFrame.grid
    print(np.array(grid.matrix))
    for r, row in enumerate(grid.matrix):
        for c, col in enumerate(row):
            if (r, c) == gf.end.xy():
                f.write("e")
            elif (r, c) == gf.start.xy():
                f.write("s")
            else:
                f.write(str(col))
        f.write("\n")
    f.close()
    
def load_state_from_file(width, height, filename="grid_save", fileform="{}_{}x{}.ssp"):
    matrix = []
    with open(fileform.format(filename, width, height), "r") as file:
        lines = list(map(lambda i:i[:-1],filter(bool, file.readlines())))
        start, end = None, None
        for r, line in enumerate(lines):
            matrix.append([])
            for c, cell in enumerate(line):
                if cell == "s":
                    start = (r, c)
                    app = 0
                elif cell == "e":
                    end = (r, c)
                    app = 0
                else:
                    app = int(cell)
                matrix[-1].append(app)
        print(matrix)
        #matrix = [list(reversed(i)) for i in np.array(matrix).transpose()]
    return matrix, start, end
            
"""
S00
110
01E
"""