import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from pathfinding.node import Node
from pathfinding.grid import Grid
import tkinter as tk

BW = 20
BH = 20
OFFSET = 5
class _Node(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class GridView(tk.Tk):

    def __init__(self, matrix = None):
        tk.Tk.__init__(self)
        if matrix is None:
            matrix = [[0] * 20] * 20
        self.grid = Grid(matrix)
        self.nodes = self.grid.nodes
        self.w = self.grid.width
        self.h = self.grid.height
        self.gridFrame = tk.Frame(self, width = BW * self.w, height = BH * self.h)
        self.start = _Node(0, 0, "green")
        self.end = _Node(self.w, self.h, "red")
        self.geometry("{width}x{height}".format(width = self.w * BW + OFFSET * 2, height = self.h * BH + OFFSET * 2))
        self.canvas = tk.Canvas(self.gridFrame)
        self.squares = []
        self.lines = []
        self.canvas.bind("<Button-1>", self.check)
        self.canvas.bind("<B1-Motion>", self.check)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.grabbing_start = False
        self.grabbing_end = False
        self.set = []
        self.gridFrame.pack(fill=tk.BOTH, expand=1)
    def drawGrid(self):
        for square in self.squares:
            self.canvas.delete(square)
        self.squares = []
        
        for y in range(self.h):
            for x in range(self.w):
                outline = "black"
                if self.grid.walkable(x, y):
                    fill = "white"
                else:
                    fill = "black"
                for square in [self.start, self.end]:
                    if (x, y) == (square.x, square.y):
                        fill = square.color
                self.squares.append(self.canvas.create_rectangle(OFFSET + x * BW, OFFSET + y * BH, OFFSET + x * BW + BW, OFFSET + y * BH + BH, outline = outline, fill = fill))
        self.canvas.pack(fill=tk.BOTH, expand=1)
        
    def drawPath(self, path):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []
        for ((x1, y1), (x2, y2)) in zip(path, path[1:]):
            self.lines.append(self.canvas.create_line(*map(lambda i: OFFSET + i * BW + BW / 2, (x1, y1, x2, y2)), fill = "blue", dash = (4, 2)))
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
            self.set.append((gx, gy))
        self.drawGrid()
        
    def release(self, event):
        self.grabbing_start = False
        self.grabbing_end = False
        self.set = []
