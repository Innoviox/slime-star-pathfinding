from math import sqrt
def octile(x, y):
    return max(x, y) + (sqrt(2)-1) * min(x, y)
