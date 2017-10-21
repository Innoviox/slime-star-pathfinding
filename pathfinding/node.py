#!/usr/bin/python
# -*- coding: utf-8 -*-


class Node(object):

<<<<<<< HEAD
    def __init__(self,x,y,walkable,parent=None):
=======
    def __init__(self,x,y,walkable,parent=None, char = '#'):
>>>>>>> 71de5995cfb2e5b73922b6783457a71e847a581b
        self.x = x
        self.y = y
        self.parent = parent

        # self.type = grid[y][x]

        self.walkable = walkable  # self.type == 0
        self.opened = False
        self.closed = False
        (self.f, self.g, self.h) = (0, 0, 0)  # cost (g + h), node to goal, start to node
<<<<<<< HEAD
=======
        self.char = char
>>>>>>> 71de5995cfb2e5b73922b6783457a71e847a581b
        
    def __lt__(self, other):
        return self.f < other.f

    def position(self):
        return [self.x, self.y]

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            return self.x == other[0] and self.y == other[1]
    def __str__(self):
        return ", ".join(map(str, reversed(self.position()))) + " " + str(self.parent)
    
<<<<<<< HEAD
    def backtrace(self):
        path = [self.position()]
        node = Node(self.x, self.y, self.walkable, self.parent)
        while node.parent:
=======
    @staticmethod
    def backtrace(node):
        path = [node.position()]
        while node.parent:
            print(node)
>>>>>>> 71de5995cfb2e5b73922b6783457a71e847a581b
            node = node.parent
            path.append(node.position())
        return list(reversed(path))
