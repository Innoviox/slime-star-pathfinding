#!/usr/bin/python
# -*- coding: utf-8 -*-
from .node import Node
import heapq
from .heuristics import octile, sqrt

class AStar(object):
    
    def __init__(self, start, end, grid, heuristic=octile):
        self.start, self.end, self.grid = start, end, grid
        self.heuristic = heuristic
    
    def find_path(self):
        return list(self.find_path_iter())[-1]
    #@staticmethod
    def find_path_iter(self):
        (open_list, closed_list) = ([self.start], [])
        self.start.g = 0
        self.start.h = 0
        self.start.f = 0
        while open_list:
            node = heapq.nsmallest(1, open_list)[0]
            open_list.remove(node)
            node.closed = True
            
            yield node.backtrace(self)
            if node == self.end:
                return #node.backtrace()
            neighbors = self.grid.neighbors(node)
            for neighbor in neighbors:
                if neighbor.closed:
                    continue
                (x, y) = neighbor.position()
                g = node.g
                if x - node.x == 0 or y - node.y == 0:
                    g += 1
                else:
                    g += sqrt(2)
                if not neighbor.opened or g < neighbor.g:
                    neighbor.g = g
                    neighbor.h = neighbor.h or self.heuristic(abs(x - self.end.x), abs(y - self.end.y))
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = node

                    if not neighbor.opened:
                        heapq.heappush(open_list, neighbor)
                        neighbor.opened = True
                    else:
                        open_list.remove(neighbor)
                        heapq.heappush(open_list, neighbor)
            #input()
        return []
    def toStr(self, path):
        return self.grid.toStr(path=path,start=self.start,end=self.end)
		
