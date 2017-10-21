#!/usr/bin/python
# -*- coding: utf-8 -*-
from .node import Node


class Grid(object):

    def __init__(self, matrix):
        self.width = len(matrix[0])
        self.height = len(matrix)
        self.matrix = matrix
        self.nodes = self.build_nodes(matrix)

    def build_nodes(self, matrix):
        nodes = [[None for i in range(self.width)] for j in
                 range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                walkable = not bool(matrix[y][x])
                nodes[y][x] = Node(x, y, walkable)
        return nodes

    def type(self, x, y):
        return self.matrix[y][x]

    def node(self, x, y):
        return self.nodes[y][x]

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y):
        return self.inside(x, y) and self.node(x, y).walkable

    def neighbors(self, node):
        neighbors = []
        sides = [False, False, False, False]  # up, down, right, left
        (x, y) = (node.x, node.y)
        for (side_num, position) in enumerate((
            (x, y + 1,),
            (x, y - 1,),
            (x + 1, y,),
            (x - 1, y,))):
            if self.walkable(*position):
                neighbors.append(self.node(*position))
                sides[side_num] = True

        # diagonals: can only go diagonally if one side around are clear

        (up, down, right, left) = sides
        diagonal_positions = []
        if up or right:
            diagonal_positions.append((x + 1, y + 1))
        if up or left:
            diagonal_positions.append((x - 1, y + 1))
        if down or right:
            diagonal_positions.append((x + 1, y - 1))
        if down or left:
            diagonal_positions.append((x - 1, y - 1))

        for position in diagonal_positions:
            if self.walkable(*position):
                neighbors.append(self.node(*position))

        return neighbors

    def toStr(self, start, end, path):
        s = '{}{}{}\n'.format(chr(9484),chr(9472) * len(self.nodes[0]),chr(9488))
        for row in self.nodes:
            s += chr(9474)
            for node in row:
                if node.walkable:
                    if node == start:
                        s += 's'
                    elif node == end:
                        s += 'e'
                    elif node.position() in path:
                        s += chr(183)
                    else:
                        s += ' '  # empty
                else:
                    s += '#'#chr(9635) # wall
            s += '{}\n'.format(chr(9474))
        s += '{}{}{}\n'.format(chr(9492),chr(9472) * len(self.nodes[0]),chr(9496))

        return s
