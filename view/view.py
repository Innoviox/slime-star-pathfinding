import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from pathfinding.node import Node
from pathfinding.grid import Grid
from pathfinding.core import AStar

import tkinter as tk

import time
from copy import deepcopy
BW = 20
BH = 20
OFFSET = 5
class _Node(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        
    def xy(self):
        return self.x, self.y
class GridFrame(tk.Frame):
    def __init__(self, master = None, matrix = None):
        if matrix is None:
            matrix = [[0 for i in range(20)] for i in range(20)]
        self.grid = Grid(matrix)
        self.nodes = self.grid.nodes
        self.w = self.grid.width
        self.h = self.grid.height
        tk.Frame.__init__(self, master, width = BW * self.w, height = BH * self.h)
        self.start = _Node(0, 0, "green")
        self.end = _Node(self.w - 1, self.h - 1, "red")
        self.canvas = tk.Canvas(self)
        self.squares = []
        self.lines = []
        self.canvas.bind("<Button-1>", self.check)
        self.canvas.bind("<B1-Motion>", self.check)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.grabbing_start = False
        self.grabbing_end = False
        self.set = []
        self.pack(fill=tk.BOTH, expand=1)
        self.touched = []
        self.ends = []
        self.solving = False
        
    def drawGrid(self):
        for square in self.squares:
            self.canvas.delete(square)
        self.squares = []
        for y in range(self.h):
            for x in range(self.w):
                outline = "black"
                if self.grid.walkable(x, y):
                    fill = "white"
                    if [x, y] in self.touched:
                        fill = "light blue"
                    if [x, y] in self.ends:
                        fill = "yellow"
                    for square in [self.start, self.end]:
                        if (x, y) == (square.x, square.y):
                            fill = square.color
                else:
                    fill = "black"

                self.squares.append(self.canvas.create_rectangle(OFFSET + x * BW, OFFSET + y * BH, OFFSET + x * BW + BW, OFFSET + y * BH + BH, outline = outline, fill = fill))
        self.canvas.pack(fill=tk.BOTH, expand=1)
        
    def drawPath(self, path):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []
        for ((x1, y1), (x2, y2)) in zip(path, path[1:]):
            self.lines.append(self.canvas.create_line(*map(lambda i: OFFSET + i * BW + BW / 2, (x1, y1, x2, y2)), fill = "red", dash = (4, 2)))
        for node in path:
            self.touched.append(node)
        for node in self.ends[:]:
            if node in path:
                self.ends.remove(node)
        self.ends.append(path[-1])
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def setStart(self, x, y):
        if self.grid.walkable(x, y):
            self.start.x = x
            self.start.y = y

    def setEnd(self, x, y):
        if self.grid.walkable(x, y):
            self.end.x = x
            self.end.y = y

    def check(self, event):
        if self.solving:
            return
        self.rte()
        ex, ey = event.x, event.y
        gx, gy = (ex - OFFSET) // BW, (ey - OFFSET) // BH
        if self.grabbing_start:
            self.setStart(gx, gy)
        elif self.grabbing_end:
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
        self.drawGrid()
        
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
    def __init__(self, matrix = None):
        tk.Tk.__init__(self)
        self.gridFrame = GridFrame(master = self, matrix = matrix)
        self.solveButton = tk.Button(self, text = "Solve!", command = self.solve)
        self.solveButton.pack()
        self.geometry("{width}x{height}".format(width = self.gridFrame.w * BW + OFFSET * 2, height = self.gridFrame.h * BH + OFFSET * 2 + 50))
        #self.resizable(False, False)
        
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
        self.gridFrame.rte()
        oldGrid = deepcopy(self.gridFrame.grid.matrix)
        for path in AStar.find_path(self.gridFrame.startNode(), self.gridFrame.endNode(), self.gridFrame.grid):
            self.drawGrid()
            self.drawPath(path)
            self.gridFrame.update()
            time.sleep(0.01)
        self.gridFrame.reset(oldGrid)
        self.drawGrid()
        self.drawPath(path)
        self.gridFrame.solving = False
