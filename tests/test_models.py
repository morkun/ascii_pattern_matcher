from unittest.mock import patch

import numpy as np
import random
import sys
from unittest import TestCase, skip

from ascii_pattern_matcher.models import (Invader, Pattern, Point, Radar, RadarMap,
                                          RectanglePattern, ScanResult)


class BaseTestCase(TestCase):
    pass


class TestPoint(BaseTestCase):

    def test_successful_init(self):
        random_int = random.randint(-sys.maxsize, sys.maxsize)

        point = Point(random_int, random_int)
        self.assertEqual(random_int, point.row_index)
        self.assertEqual(random_int, point.column_index)

    def test_fail_init(self):
        random_float = random.random()

        self.assertRaises(Exception, lambda: Point(random_float, random_float))


class TestPattern(BaseTestCase):

    klass = Pattern

    def test_successful_init(self):
        random_arr = np.random.rand(3, 2)

        pattern = self.klass(random_arr)
        self.assertTrue(np.all(pattern.get_pattern() == random_arr))

    def test_fail_init(self):
        random_float = random.random()
        self.assertRaises(Exception, lambda: self.klass(random_float))

        random_int = random.randint(-sys.maxsize, sys.maxsize)
        self.assertRaises(Exception, lambda: self.klass(random_int))

        n = 5
        random_2d_array = [[random.random() for i in range(n)] for j in range(n)]
        # 2d array but not np array
        self.assertRaises(Exception, lambda: self.klass(random_2d_array))

    def test_get_pattern(self):
        random_arr = np.random.rand(3, 2)

        pattern = self.klass(random_arr)
        _pattern = pattern.get_pattern()
        self.assertTrue(isinstance(_pattern, np.ndarray))
        self.assertEqual(2, len(_pattern.shape))

    def test_get_area(self):
        random_arr = np.random.rand(3, 2)

        pattern = self.klass(random_arr)
        self.assertRaises(NotImplementedError, lambda: pattern.get_area())


class TestRectanglePattern(TestPattern):
    klass = RectanglePattern
    RANDOM_MIN = 5
    RANDOM_MAX = 10

    def generate_reasonable_random_dimensions(self):
        random_row = random.randint(self.RANDOM_MIN, self.RANDOM_MAX)
        random_column = random.randint(self.RANDOM_MIN, self.RANDOM_MAX)
        return random_row, random_column

    def test_get_area(self):
        random_row, random_column = self.generate_reasonable_random_dimensions()
        random_arr = np.random.rand(random_row, random_column)

        rectangle_p = self.klass(random_arr)
        self.assertEqual(random_row * random_column, rectangle_p.get_area())

    def test_dimensions(self):
        random_row, random_column = self.generate_reasonable_random_dimensions()
        random_arr = np.random.rand(random_row, random_column)

        p = self.klass(random_arr)
        self.assertEqual((random_row, random_column), p.get_dimensions())

    def test_get_sliced_pattern(self):
        # TODO more tests
        random_row, random_column = self.generate_reasonable_random_dimensions()
        random_arr = np.random.rand(random_row, random_column)

        rectangle_p = self.klass(random_arr)
        point = Point(0, 0)

        # whole pattern
        sliced = rectangle_p.get_sliced_pattern(point, random_row, random_column)
        self.assertTrue(np.all(sliced.get_pattern() == random_arr))

        # quarter
        half_row = round(random_row/2)
        half_column = round(random_column/2)
        sliced = rectangle_p.get_sliced_pattern(point, half_row, half_column)
        self.assertEqual(half_row * half_column, sliced.get_area())
        self.assertEqual((half_row, half_column), sliced.get_dimensions())
        self.assertTrue(np.all(sliced.get_pattern() == random_arr[0:half_row, 0:half_column]))


class TestInvader(TestRectanglePattern):
    klass = Invader

    def test_get_covered_area(self):
        random_row, random_column = self.generate_reasonable_random_dimensions()

        # all zeros so covered area will be zero
        random_arr = np.zeros(random_row * random_column).reshape((random_row, random_column))
        invader = self.klass(random_arr)
        self.assertEqual(0, invader.get_covered_area())

        # all ones so covered area will be actual area
        random_arr = np.ones(random_row * random_column).reshape((random_row, random_column))
        invader = self.klass(random_arr)
        self.assertEqual(random_row * random_column, invader.get_covered_area())

        # only one is 1 so covered area will be 1
        random_arr = np.zeros(random_row * random_column).reshape((random_row, random_column))
        random_arr[0][0] = 1
        invader = self.klass(random_arr)
        self.assertEqual(1, invader.get_covered_area())

        # first row is ones so covered area will be column number
        random_arr = np.zeros(random_row * random_column).reshape((random_row, random_column))
        random_arr[0] = np.ones(random_column)
        invader = self.klass(random_arr)
        self.assertEqual(random_column, invader.get_covered_area())


class TestRadarMap(TestRectanglePattern):
    klass = RadarMap
    pass


class TestScanResult(BaseTestCase):

    def test_successful_init(self):
        random_int = random.randint(-sys.maxsize, sys.maxsize)

        point = Point(random_int, random_int)
        scan_result = ScanResult(point, random_int)
        self.assertEqual(random_int, scan_result.invader_index)
        self.assertEqual(point, scan_result.point)

    def test_fail_init(self):
        random_int = random.randint(-sys.maxsize, sys.maxsize)
        random_float = random.random()

        self.assertRaises(Exception, lambda: ScanResult(random_int, random_float))
        self.assertRaises(Exception, lambda: ScanResult(random_float, random_int))


class TestRadar(BaseTestCase):
    CREATE_FOR_INVADER = 'I'
    CREATE_FOR_MAP = 'M'

    RANDOM_MAP_MIN = 50
    RANDOM_MAP_MAX = 100
    RANDOM_INVADER_MIN = 5
    RANDOM_INVADER_MAX = 10

    ACCURACY = 0.8

    def generate_reasonable_random_dimensions(self, create_for=None):
        min_val, max_val = self.RANDOM_MAP_MIN, self.RANDOM_MAP_MAX
        if create_for == self.CREATE_FOR_INVADER:
            min_val, max_val = self.RANDOM_INVADER_MIN, self.RANDOM_INVADER_MAX
        random_row = random.randint(min_val, max_val)
        random_column = random.randint(min_val, max_val)
        return random_row, random_column

    def test_successful_init(self):
        random_float = random.random()

        radar = Radar(random_float)
        self.assertEqual(random_float, radar.accuracy)

    def test_fail_init(self):
        # inaccurate float
        random_float = random.uniform(1, 10)
        self.assertRaises(Exception, lambda: Radar(random_float))

        # invalid type
        random_int = random.randint(-sys.maxsize, sys.maxsize)
        self.assertRaises(Exception, lambda: Radar(random_int))

    def test_is_match(self):  # also for get_match_probability_exceptions
        radar = Radar(self.ACCURACY)

        random_row = random.randint(5, 10)
        random_column = random.randint(5, 10)
        random_arr = np.ones(random_row * random_column).reshape((random_row, random_column))
        invader = Invader(random_arr)
        map_slice = RectanglePattern(random_arr)

        # same dimension
        probability = radar.get_match_probability(invader, map_slice)
        self.assertEqual(1, probability)  # because they are all ones
        is_match = radar.is_match(invader, map_slice)
        self.assertTrue(is_match)

        # different dimensions
        smaller_arr = np.random.rand(random_row-1, random_column-1)
        map_slice = RectanglePattern(smaller_arr)
        self.assertRaises(Exception, lambda: radar.get_match_probability(invader, map_slice))
        self.assertRaises(Exception, lambda: radar.is_match(invader, map_slice))

        # invalid types
        self.assertRaises(Exception, lambda: radar.get_match_probability(map_slice, map_slice))
        self.assertRaises(Exception, lambda: radar.get_match_probability(invader, Pattern(smaller_arr)))
        self.assertRaises(Exception, lambda: radar.is_match(map_slice, map_slice))
        self.assertRaises(Exception, lambda: radar.is_match(invader, Pattern(smaller_arr)))

    @patch('ascii_pattern_matcher.models.Radar.scan_for_invader')
    def test_scan(self, _scan_for_invader):
        radar = Radar(self.ACCURACY)
        random_arr = np.random.rand(2, 5)

        number_of_invaders = 5
        for i in range(number_of_invaders):
            radar.add_known_invader(random_arr)

        radar.scan()
        self.assertEqual(number_of_invaders, _scan_for_invader.call_count)

    @patch('ascii_pattern_matcher.models.Radar.is_match')
    def test_scan_for_invader(self, _is_match):
        radar = Radar(self.ACCURACY)
        invader_row_num = 2
        invader_col_num = 5
        random_arr = np.random.rand(invader_row_num, invader_col_num)

        # init invaders
        number_of_invaders = 3
        for i in range(number_of_invaders):
            radar.add_known_invader(random_arr)

        # init map
        map_row_num = 20
        map_col_num = 30
        random_arr = np.random.rand(map_row_num, map_col_num)
        radar.set_radar_map(random_arr)

        area_to_be_scanned = (map_row_num - invader_row_num) * (map_col_num - invader_col_num)

        for i in range(number_of_invaders):
            radar.scan_for_invader(i)
            self.assertEqual(area_to_be_scanned * (i + 1), _is_match.call_count)

    @skip
    def test_add_known_invader(self):
        # no need to test
        pass

    @skip
    def test_set_radar_map(self):
        # no need to test
        pass

    def test_init_from_file(self):
        # TODO write InputFileHandler and reuse
        pass

    def test_get_cleaned_map(self):
        # TODO
        pass

    def test_get_printable_map(self):
        # TODO write test_get_cleaned_map first
        pass

    def test_dump_to_file(self):
        # TODO write OutputFileHandler and reuse
        pass

