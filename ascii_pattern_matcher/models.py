from typing import Tuple

import numpy as np

from ascii_pattern_matcher.utils import InputFileHandler, SampleHandler, OutputFileHandler


class Point:
    """
    Stores indices of 2D np array.
    Used to store locations of Patterns.
    """
    row_index = None
    column_index = None

    def __init__(self, row_index: int, column_index: int):
        if not isinstance(row_index, int) or not isinstance(column_index, int):
            # TODO define improper configuration exception
            raise Exception
        self.row_index = row_index
        self.column_index = column_index


class Pattern:
    """
    Stores 2D np array.
    Used to store and process ASCII pattern samples which is processed to zero and ones.
    """
    _pattern = None

    def __init__(self, pattern: np.ndarray):
        if not isinstance(pattern, np.ndarray):
            raise Exception
        if len(pattern.shape) != 2:
            raise Exception
        self._pattern = pattern

    def get_pattern(self):
        return self._pattern

    def get_area(self):
        raise NotImplementedError


class RectanglePattern(Pattern):
    """
    Stores 2D rectangular shaped np array.
    Used to store Invaders and Radar sample
    """

    def get_dimensions(self) -> Tuple:
        return self._pattern.shape

    def get_area(self) -> int:
        row_num, column_num = self.get_dimensions()
        return row_num * column_num

    def get_sliced_pattern(self, point: Point, row_offset: int, col_offset: int):
        """
        Returns the sliced pattern starting from the given point as the top left of the slice

        :return: Sliced pattern in the format of the given object
        """
        # TODO handle irrelevent inputs
        row_idx = point.row_index
        col_idx = point.column_index
        return self.__class__(self.get_pattern()[row_idx:row_idx + row_offset, col_idx:col_idx + col_offset])


class Invader(RectanglePattern):

    def get_covered_area(self) -> int:
        """
        Returns sum of the positive signals within the pattern. The actual area in the 2D space.
        It is used to have a more accurate pattern matching.
        """
        return np.sum(self.get_pattern())


class RadarMap(RectanglePattern):
    pass


class ScanResult:
    """
    Stores the location and the type of the Invader on the RadarMap
    """
    point = None
    invader_index = None

    def __init__(self, point: Point, invader_index: int):
        if not isinstance(point, Point) or not isinstance(invader_index, int):
            raise Exception
        self.point = point
        self.invader_index = invader_index


class Radar:
    """
    Main controller to handle initialization, scanning and reporting.
    """
    accuracy = None
    radar_map = None
    known_invaders = []
    scan_results = []

    def __init__(self, accuracy: float):
        if not isinstance(accuracy, float):
            raise Exception
        if not (0 < accuracy < 1):
            raise Exception
        self.accuracy = accuracy

    def add_known_invader(self, invader_sample: np.ndarray):
        self.known_invaders.append(Invader(invader_sample))

    def set_radar_map(self, radar_map_sample: np.ndarray):
        self.radar_map = RadarMap(radar_map_sample)

    def init_from_file(self, file_path: str):
        handler = InputFileHandler(file_path)

        for invader_sample in handler.get_known_invader_samples():
            self.add_known_invader(invader_sample)

        self.set_radar_map(handler.get_radar_sample())

    def get_match_probability(self, invader: Invader, map_slice: RectanglePattern) -> float:
        """
        Takes invader and a rectangle pattern, and compare if they match together
        """
        if not isinstance(invader, Invader) or not isinstance(map_slice, RectanglePattern):
            raise Exception
        if invader.get_dimensions() != map_slice.get_dimensions():
            raise Exception
        covered_area = invader.get_covered_area()
        matched_area = np.sum(np.logical_and(invader.get_pattern(), map_slice.get_pattern()))
        return matched_area / covered_area

    def is_match(self, invader: Invader, map_slice: RectanglePattern) -> bool:
        probability = self.get_match_probability(invader, map_slice)
        return probability >= self.accuracy

    def add_scan_result(self, point: Point, invader_index: int):
        self.scan_results.append(ScanResult(point, invader_index))

    def scan_for_invader(self, invader_index: int):
        invader = self.known_invaders[invader_index]

        map_row_num, map_col_num = self.radar_map.get_dimensions()
        invader_row_num, invader_col_num = invader.get_dimensions()

        # TODO come up with a better way instead of traversing the whole map
        """
            TODO what about edges?
            Option 1: User padding (more efficient, less accurate)
            1- Add padding to edges with zeros (maximum biggest invader's half size)
            2- Decrease the accuracy while processing edges
            3- Create the printable map as usual
            3- Slice the actual portion while exporting to file
            Option 2: Extra steps on edges (more accurate, more work)
            1- Create smaller portions of given invaders (minimum quarter size)
            2- Check with smaller invaders on edges with the same accuracy 
        """
        for row_idx in range(map_row_num - invader_row_num):
            for col_idx in range(map_col_num - invader_col_num):
                # exclude invader's sizes
                point = Point(row_idx, col_idx)  # utilizes the top-left point of invader area not center
                map_slice = self.radar_map.get_sliced_pattern(point, invader_row_num, invader_col_num)
                if self.is_match(invader, map_slice):
                    self.add_scan_result(point, invader_index)

    def scan(self):
        for invader_index in range(len(self.known_invaders)):
            self.scan_for_invader(invader_index)

    def get_cleaned_map(self) -> np.ndarray:
        map_row_num, map_col_num = self.radar_map.get_dimensions()
        result_map = np.zeros((map_row_num, map_col_num))
        for scan_result in self.scan_results:
            invader = self.known_invaders[scan_result.invader_index]
            row_idx, col_idx = scan_result.point.row_index, scan_result.point.column_index
            invader_row_num, invader_col_num = invader.get_dimensions()
            result_map[row_idx:row_idx + invader_row_num, col_idx:col_idx + invader_col_num] = invader.get_pattern()
        return result_map

    def get_printable_map(self):
        return SampleHandler().characterize_sample(self.get_cleaned_map())

    def dump_to_file(self, file_path: str):
        handler = OutputFileHandler(file_path)
        printable_map = self.get_printable_map()
        handler.dump_file_content(printable_map)
