class Memento:
    def __init__(self, color, position):
        self._color = color
        self._position = position.copy()

    def get_color(self):
        return self._color

    def get_position(self):
        return self._position.copy()