import unittest
from engine.utils import math_utils


class TestMathUtils(unittest.TestCase):

    def test_distance_formula_basic(self):
        x1 = 9
        y1 = 7
        x2 = 3
        y2 = 2

        dist = math_utils.distance_formula(x1, y1, x2, y2)

        self.assertAlmostEqual(dist, 7.8102, places=4)

    def test_distance_formula_complex(self):
        x1 = 3.45
        y1 = 14.145
        x2 = 16.32
        y2 = 2.134

        dist = math_utils.distance_formula(x1, y1, x2, y2)

        self.assertAlmostEqual(dist, 17.604, places=4)

    def test_gradient(self):
        x1 = 3
        y1 = 3
        x2 = 5
        y2 = -1
        
        self.assertAlmostEqual(math_utils.gradient(x1, y1, x2, y2), -2)

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
        current_x = 0
        current_y = 1
        x1 = 1
        y1 = 1
        x2 = 5
        y2 = 5

        closest = math_utils.get_closest_point(current_x, current_y, x1, y1, x2, y2)

        self.assertEqual((x1, y1), closest)

    def test_get_closest_point_negatives(self):
        current_x = 0
        current_y = 1
        x1 = -1
        y1 = -1
        x2 = 5
        y2 = 5

        closest = math_utils.get_closest_point(current_x, current_y, x1, y1, x2, y2)

        self.assertEqual((x1, y1), closest)

    def test_get_closest_point_partial_coords(self):
        current_x = 0
        current_y = 1
        x1 = -1
        y1 = None
        x2 = 5
        y2 = 5

        closest = math_utils.get_closest_point(current_x, current_y, x1, y1, x2, y2)

        self.assertEqual((x2, y2), closest)

        current_x = 0
        current_y = 1
        x1 = -1
        y1 = -1
        x2 = 5
        y2 = None

        closest = math_utils.get_closest_point(current_x, current_y, x1, y1, x2, y2)

        self.assertEqual((x1, y1), closest)

    def test_get_new_coordinates(self):
        """
        Test that in a basic case we get the correct next coordinates. If this fails, the
        formula is very wrong.
        :return:
        """

        current_x = 0
        current_y = 0

        angle = 0.785398  # 45 degrees

        speed = 5

        expected_x = 3.535
        expected_y = 3.535
        res_x, res_y = math_utils.get_new_coordinates(current_x, current_y, angle, speed)

        self.assertAlmostEqual(expected_x, res_x, places=2)
        self.assertAlmostEqual(expected_y, res_y, places=2)

    def test_get_new_coordinates_along_x_axis(self):
        """
        In this case the angle is 0, so the next coordinate shouldn't vary on the y
        axis.
        """

        current_x = 0
        current_y = 0

        angle = 0.0

        speed = 5

        expected_x = 5
        expected_y = 0

        res_x, res_y = math_utils.get_new_coordinates(current_x, current_y, angle, speed)

        self.assertAlmostEqual(expected_x, res_x, places=2)
        self.assertAlmostEqual(expected_y, res_y, places=2)

    def test_get_new_coordinates_along_y_axis(self):
        """
        In this case the angle is equal to 90 degrees, so the next coordinates should
        vary only on the y axis.
        """

        current_x = 0
        current_y = 0

        angle = 1.5708

        speed = 5

        expected_x = 0
        expected_y = 5

        res_x, res_y = math_utils.get_new_coordinates(current_x, current_y, angle, speed)

        self.assertAlmostEqual(expected_x, res_x, places=2)
        self.assertAlmostEqual(expected_y, res_y, places=2)

    def test_get_new_coordinates_negative_speed(self):
        """
        Get new coordinates should also work on negative speeds (i.e. moving backwards)
        :return:
        """

        current_x = 0
        current_y = 0

        angle = 0.785398  # 45 degrees

        speed = -5

        expected_x = -3.535
        expected_y = -3.535
        res_x, res_y = math_utils.get_new_coordinates(current_x, current_y, angle, speed)

        self.assertAlmostEqual(expected_x, res_x, places=2)
        self.assertAlmostEqual(expected_y, res_y, places=2)


if __name__ == '__main__':
    unittest.main()

