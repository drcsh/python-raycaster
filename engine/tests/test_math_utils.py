import unittest
import math
from engine import math_utils


class TestMathUtils(unittest.TestCase):

    def test_distance_formula_basic(self):
        x1 = 9
        y1 = 7
        x2 = 3
        y2 = 2

        dist = math_utils.distance_formula((x1, y1), (x2, y2))

        self.assertAlmostEqual(dist, 7.8102, places=4)

    def test_distance_formula_complex(self):
        x1 = 3.45
        y1 = 14.145
        x2 = 16.32
        y2 = 2.134

        dist = math_utils.distance_formula((x1, y1), (x2, y2))

        self.assertAlmostEqual(dist, 17.604, places=4)

    def test_get_y_for_x(self):

        m = 1.234
        x = 6.1
        b = 3

        y = math_utils.get_y_for_x(x, m, b)

        self.assertAlmostEqual(y, 10.5274, places=4)

    def test_get_x_for_y(self):
        y = 10.5274
        m = 1.234
        b = 3

        x = math_utils.get_x_for_y(y, m, b)

        self.assertAlmostEqual(x, 6.1)

    def test_get_closest_point(self):
        origin = (0, 0)
        p1 = (1, 1)
        p2 = (5, 5)

        closest = math_utils.get_closest_point(origin, p1, p2)

        self.assertEqual(p1, closest)

    def test_get_closest_point_negatives(self):
        origin = (0, 0)
        p1 = (-1, -1)
        p2 = (5, 5)

        closest = math_utils.get_closest_point(origin, p1, p2)

        self.assertEqual(p1, closest)

    def test_get_closest_point_partial_coords(self):
        origin = (0, 0)
        p1 = (None, 1)
        p2 = (5, 5)

        closest = math_utils.get_closest_point(origin, p1, p2)

        self.assertEqual(p2, closest)

        origin = (0, 0)
        p1 = (-1, -1)
        p2 = (None, 5)

        closest = math_utils.get_closest_point(origin, p1, p2)

        self.assertEqual(p1, closest)


if __name__ == '__main__':
    unittest.main()

