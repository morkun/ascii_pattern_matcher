import numpy as np


class Point:
    row_index = None
    column_index = None

    def __init__(self, row_index: int, column_index: int):
        self.row_index = row_index
        self.column_index = column_index


class Pattern:
    _pattern = None

    def __init__(self, pattern: np.ndarray):
        self._pattern = pattern

    def get_pattern(self):
        return self._pattern

    def get_area(self):
        raise NotImplementedError


class RectanglePattern(Pattern):

    def get_dimensions(self):
        return self._pattern.shape

    def get_area(self) -> int:
        # TODO can be used as number of elements, new method?
        row_num, column_num = self.get_dimensions()
        return row_num * column_num


class Invader(RectanglePattern):
    pass


class RadarMap(RectanglePattern):
    pass


class Radar:
    accuracy = None
    radar_map = None
    known_invaders = []

    def __init__(self, accuracy: float):
        self.accuracy = accuracy

    def add_known_invader(self, invader: Invader):
        self.known_invaders.append(invader)

    def set_radar_map(self, radar_map: RadarMap):
        self.radar_map = radar_map

    def scan_for_invader(self, invader_index: int):
        pass

    def scan(self):
        pass
