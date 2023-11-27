import math

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def abs(self):
        result = math.sqrt(self.x ** 2 + self.y ** 2)
        return round(result * 100.0) / 100.0

    def cdot(self, param):
        components = param.get_components()
        return self.x * components[0] + self.y * components[1]

    def get_components(self):
        return [self.x, self.y]