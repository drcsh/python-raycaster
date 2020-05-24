import math


def distance_formula(point_1, point_2):
    """
    Distance between two points is defined as the square root of (x2 - x1)^2 + (y2 - y1) ^ 2

    :param tuple(float, float) point_1:
    :param tuple(float, float) point_2:
    :return: distance
    :rtype float:
    """
    x1 = point_1[0]
    y1 = point_1[1]

    x2 = point_2[0]
    y2 = point_2[1]

    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def get_y_for_x(x, gradient, y_intercept):
    """
    Linear equation, y = mx + c

    :param float x:
    :param float gradient:
    :param float y_intercept:
    :return:
    """
    return (x * gradient) + y_intercept


def get_x_for_y(y, gradient, y_intercept):
    """
    Linear equation reorganised, x = (y - c) / m
    :param float y:
    :param float gradient:
    :param float y_intercept:
    :return:
    """
    return (y - y_intercept) / gradient