import numpy as np

from ascii_pattern_matcher.utils import InputFileHandler, SampleHandler, OutputFileHandler


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

    def get_sliced_pattern(self, point: Point, row_offset: int, col_offset: int):
        row_idx = point.row_index
        col_idx = point.column_index
        return RectanglePattern(self.get_pattern()[row_idx:row_idx + row_offset, col_idx:col_idx + col_offset])


class Invader(RectanglePattern):
    pass


class RadarMap(RectanglePattern):
    pass


class ScanResult:
    point = None
    invader_index = None

    def __init__(self, point: Point, invader_index: int):
        self.point = point
        self.invader_index = invader_index


class Radar:
    accuracy = None
    radar_map = None
    known_invaders = []
    scan_results = []

    def __init__(self, accuracy: float):
        self.accuracy = accuracy

    def add_known_invader(self, invader: Invader):
        self.known_invaders.append(invader)

    def set_radar_map(self, radar_map: RadarMap):
        self.radar_map = radar_map

    def init_from_file(self, file_path: str):
        handler = InputFileHandler(file_path)

        for invader_sample in handler.get_known_invader_samples():
            self.add_known_invader(Invader(invader_sample))

        self.set_radar_map(RadarMap(handler.get_radar_sample()))

    def get_match_probability(self, pattern1: Invader, pattern2: Pattern) -> float:
        # TODO another class?
        # TODO handle irrelevant inputs
        number_of_element = pattern1.get_area()
        number_of_equal_elements = np.sum(pattern1.get_pattern() == pattern2.get_pattern())
        # TODO only check positive signals?
        return number_of_equal_elements / number_of_element

    def is_match(self, pattern1: Invader, pattern2: Pattern) -> bool:
        probability = self.get_match_probability(pattern1, pattern2)
        return probability >= self.accuracy

    def add_scan_result(self, point: Point, invader_index: int):
        self.scan_results.append(ScanResult(point, invader_index))

    def scan_for_invader(self, invader_index: int):
        invader = self.known_invaders[invader_index]

        map_row_num, map_col_num = self.radar_map.get_dimensions()
        invader_row_num, invader_col_num = invader.get_dimensions()

        # TODO other than two dimensions?
        for row_idx in range(map_row_num - invader_row_num):
            # TODO come up with a better way instead of traversing the whole map
            # TODO what about edges?
            for col_idx in range(map_col_num - invader_col_num):
                point = Point(row_idx, col_idx)
                map_slice = self.radar_map.get_sliced_pattern(point, invader_row_num, invader_col_num)
                if self.is_match(invader, map_slice):
                    self.add_scan_result(point, invader_index)
                elif row_idx in [0, map_row_num]:
                    pass

    def scan(self):
        # TODO is rotation important?
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
