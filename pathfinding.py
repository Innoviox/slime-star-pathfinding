#!/usr/bin/python
# -*- coding: utf-8 -*-
from node import Node
import heapq
from math import sqrt


def octile(x, y):
    return max(x, y) + (sqrt(2)-1) * min(x, y)


class AStar(object):

    @staticmethod
    def find_path(start, end, grid, max_runs=0):
        (open_list, closed_list) = ([start], [])
        start.g = 0
        start.h = 0
        start.f = 0
        while open_list:
            node = heapq.nsmallest(1, open_list)[0]
            open_list.remove(node)
            node.closed = True
            if node == end:
                return Node.backtrace(node)
            neighbors = grid.neighbors(node)
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
                    neighbor.h = neighbor.h or octile(abs(x - end.x), abs(y - end.y))
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



			
