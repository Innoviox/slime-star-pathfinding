class Path (object):
    def __init__(self, path, astar):
        self.path = path
        self.astar = astar
    def __repr__(self):
        return self.astar.toStr(self.path)
    def __str__(self):
        return repr(self)
