import sys
sys.path.append('..')

from pathfinding.util         import file as f
from pathfinding.core.grid    import Grid
from pathfinding.core.finders import AStar

import tkinter as tk

from copy import deepcopy
BW = 20
BH = 20
OFFSET = 5
FRAMES = 10
class _Node(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color        
    def xy(self):
        return self.x, self.y
class GridFrame(tk.Frame):
    def __init__(self, master = None, matrix = None, dw = 1200 // BW - 10, dh = 800 // BH - 10, start=None, end=None):
        if matrix is None:
            matrix = [[0 for i in range(dw)] for i in range(dh)]
        self.grid = Grid(matrix)
        self.nodes = self.grid.nodes
        self.w = self.grid.width
        self.h = self.grid.height
        tk.Frame.__init__(self, master, width = OFFSET + BW * self.w, height = OFFSET + BH * self.h)
        if start is None:
            self.start = _Node(0, 0, "green")
        else:
            self.start = _Node(start[0], start[1], "green")
        
        if end is None:
            self.end = _Node(self.w - 1, self.h - 1, "red")
        else:
            self.end = _Node(end[0], end[1], "red")
        self.canvas = tk.Canvas(self, width = OFFSET + BW * self.w, height = OFFSET + BH * self.h)
        self.squares = {}
        self.lines = []
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.grabbing_start = False
        self.grabbing_end = False
        self.set = []
        self.touched = []
        self.ends = []
        self.solving = False
        self.changing = {}
        self.checked = True
        self.drawnFirst = False
        self.ose = []
    def drawDefaultGrid(self):
        self.drawnFirst = True
        for y in range(self.h):
            for x in range(self.w):
                outline = "black"
                if self.grid.walkable(x, y):
                    fill = "white"
                    for square in [self.start, self.end]:
                        if (x, y) == (square.x, square.y):
                            fill = square.color
                else:
                    fill = "black"
                p1, p2, p3, p4 = OFFSET + x * BW, OFFSET + y * BH, OFFSET + x * BW + BW, OFFSET + y * BH + BH
                self.squares[(x, y)] = self.canvas.create_rectangle(p1, p2, p3, p4, outline = outline, fill = fill)
    def drawGrid(self):
        #for square in self.squares:
#            self.canvas.delete(square)
#        self.squares = []
        toDraw = []
        if self.grabbing_start or self.grabbing_end:
            for (x, y) in [i for i in self.ose]:
                p1, p2, p3, p4 = OFFSET + x * BW, OFFSET + y * BH, OFFSET + x * BW + BW, OFFSET + y * BH + BH
                self.squares[(x, y)] = self.canvas.create_rectangle(p1, p2, p3, p4, outline = "black", fill = "white")
                self.ose.remove((x, y))
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self.changing.keys() or [x, y] in self.touched or [x, y] in self.ends or (x, y) in [self.start.xy(), self.end.xy()]:
                    self.canvas.delete(self.squares[(x, y)])
                    outline = "black"
                    if self.grid.walkable(x, y):
                        fill = "white"
                        if [x, y] in self.touched:
                            fill = "light blue"
                            self.touched.remove([x, y])
                        if [x, y] in self.ends:
                            fill = "yellow"
                            self.ends.remove([x, y])
                        for square in [self.start, self.end]:
                            if (x, y) == (square.x, square.y):
                                fill = square.color
                    else:
                        fill = "black"
                    p1, p2, p3, p4 = OFFSET + x * BW, OFFSET + y * BH, OFFSET + x * BW + BW, OFFSET + y * BH + BH
                    if (x, y) in self.changing.keys():
                        n = self.changing[(x, y)]
                        p1, p2, p3, p4 = OFFSET + x * BW, OFFSET + y * BH, OFFSET + x * BW + BW, OFFSET + y * BH + BH,
                        e = [FRAMES - n, n][n < FRAMES / 2]
                        p1 -= e
                        p2 -= e
                        p3 += e
                        p4 += e
                        self.changing[(x, y)] -= 1
                        if n == 0:
                            self.changing.pop((x, y))
                        toDraw.append((x, y, p1, p2, p3, p4, outline, fill))
                    else:
                        self.squares[(x, y)] = self.canvas.create_rectangle(p1, p2, p3, p4, outline = outline, fill = fill)
        for (x, y, p1, p2, p3, p4, outline, fill) in toDraw:
            self.canvas.delete(self.squares[(x, y)])
            self.squares[(x, y)] = self.canvas.create_rectangle(p1, p2, p3, p4, outline = outline, fill = fill)

        self.canvas.pack(fill=tk.BOTH, expand=1)        
    def drawPath(self, path):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []
        for ((x1, y1), (x2, y2)) in zip(path.path, path.path[1:]):
            self.lines.append(self.canvas.create_line(*map(lambda i: OFFSET + i * BW + BW / 2, (x1, y1, x2, y2)), fill = "red", dash = (4, 2)))
        for node in path.path:
            self.touched.append(node)
        for node in self.ends[:]:
            if node in path.path:
                self.ends.remove(node)
        self.ends.append(path.path[-1])
        self.canvas.pack(fill=tk.BOTH, expand=1)
    def setStart(self, x, y):
        if self.grid.walkable(x, y):
            self.start.x = x
            self.start.y = y
    def setEnd(self, x, y):
        if self.grid.walkable(x, y):
            self.end.x = x
            self.end.y = y
    def click(self, event):
        self.checked = True
        self.move(event)
    def move(self, event):
        if self.solving:
            return
        self.rte()
        ex, ey = event.x, event.y
        gx, gy = self.getPosition(event)
        if self.grabbing_start:
            self.ose.append(self.start.xy())
            self.setStart(gx, gy)
        elif self.grabbing_end:
            self.ose.append(self.end.xy())
            self.setEnd(gx, gy)
        elif (gx, gy) == (self.start.x, self.start.y):
            self.grabbing_start = True
        elif (gx, gy) == (self.end.x, self.end.y):
            self.grabbing_end = True            
        elif (gx, gy) not in self.set and self.grid.inside(gx, gy):
            w = self.grid.node(gx, gy).walkable
            self.grid.node(gx, gy).walkable = not w
            self.grid.matrix[gy][gx] = int(w)
            self.set.append((gx, gy))
            self.changing[(gx, gy)] = FRAMES
    def getPosition(self, event):
        return (event.x - OFFSET) // BW, (event.y - OFFSET) // BH
    def release(self, event):
        self.grabbing_start = False
        self.grabbing_end = False
        self.set = []
    def startNode(self):
        return self.grid.node(*self.start.xy())    
    def endNode(self):
        return self.grid.node(*self.end.xy())
    def reset(self, grid):
        self.grid = Grid(grid)
    def rte(self):
        self.touched = []
        self.ends = []
        
class GridView(tk.Tk):
    def __init__(self, matrix = None, dw = 1200 // BW - 10, dh = 800 // BH - 10, start=None, end=None, filename="grid_save"):
        tk.Tk.__init__(self)
        self.gridFrame = GridFrame(master = self, matrix = matrix, dw=dw, dh=dh, start=start, end=end)
        self.gridFrame.grid_configure(columnspan = 3)
        self.solveButton = tk.Button(self, text = "Solve", command = self.solve)
        self.solveButton.grid_configure(column = 0, row = 1)
        self.stopButton = tk.Button(self, text = "Stop", command = self.stop)
        self.stopButton.grid_configure(column = 1, row = 1)
        self.clearButton = tk.Button(self, text = "Clear", command = self.clear)
        self.clearButton.grid_configure(column = 2, row = 1)
        self.saveButton = tk.Button(self, text = "Save", command = lambda fn=filename: f.save_state_to_file(self, filename=fn))
        self.saveButton.grid_configure(column = 2, row = 2)
        self.geometry("{width}x{height}".format(width = self.gridFrame.w * BW + OFFSET * 2, height = self.gridFrame.h * BH + OFFSET * 2 + 50))
        self.omatrix = deepcopy(self.gridFrame.grid.matrix)
        self.drawGridId = False       
    def drawGrid(self):
        self.gridFrame.drawGrid()      
    def drawPath(self, path):
        self.gridFrame.drawPath(path)
    def setStart(self, x, y):
        self.gridFrame.setStart(x, y)
    def setEnd(self, x, y):
        self.gridFrame.setEnd(x, y)
    def solve(self):
        self.gridFrame.solving = True
        self.gridFrame.checked = False
        self.gridFrame.rte()
        self.gridFrame.drawDefaultGrid()
        oldGrid = deepcopy(self.gridFrame.grid.matrix)
        self.after_cancel(self.drawGridId)
        self.drawGridId = False
        for path in AStar(self.gridFrame.startNode(), self.gridFrame.endNode(), self.gridFrame.grid).find_path_iter():
            if not self.gridFrame.solving: return
            self.drawGrid()
            self.drawPath(path)
            self.gridFrame.update()
        self.gridFrame.reset(oldGrid)
        self.drawPath(path)
        self.gridFrame.solving = False
    def stop(self):
        self.gridFrame.solving = not self.gridFrame.solving
        #self.gridFrame.rte()
        
    def clear(self):
        if not self.gridFrame.solving:
            self.gridFrame.reset(self.omatrix)
            self.gridFrame.drawnFirst = False
    def mainloop(self):
        while 1:
            if not self.gridFrame.drawnFirst:
                self.gridFrame.drawDefaultGrid()
            elif self.gridFrame.checked:
                self.drawGrid()
            self.update_idletasks()
            self.update()
