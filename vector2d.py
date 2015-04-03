from math import sqrt

class Vector2D(object):
    def __init__(self, x, y=None):
        if y == None:
            self.x = float(x.x)
            self.y = float(x.y)
        else:
            self.x = float(x)
            self.y = float(y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __repr__(self):
        return 'x=' + str(self.x) + ', y=' + str(self.y)

    def norm(self):
        m = self.mag()
        if m == 0: return Vector2D(0,0)
        return Vector2D(self.x / m, self.y / m)

    def magsqr(self):
        return self.x ** 2 + self.y ** 2

    def mag(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __iter__(self):
        yield self.x
        yield self.y

    length = property(fget=mag)
