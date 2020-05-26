import math


def distance_formula(x1, y1, x2, y2):
    """
    Distance between two points is defined as the square root of (x2 - x1)^2 + (y2 - y1) ^ 2

    :param float x1:
    :param float y1:
    :param float x2:
    :param float y2:
    :return: distance
    :rtype float:
    :raises TypeError: Any of the values are non-numeric or None.
    """
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


def get_closest_point(current_x, current_y, p1_x, p1_y, p2_x, p2_y):
    """
    Given a current position and two other positions which we're interested in, works out which of the two is
    closest to the current position.

    If 1 of the POIs is partial (contains a None), the other will be returned. If both are None, the second POI will
    be returned, but this behavior should be considered undefined.
    
    :param float current_x:
    :param float current_y:
    :param float|None p1_x: x of the first POI
    :param float|None p1_y:
    :param float|None p2_x: x of the second POI
    :param float|None p2_y:
    :return: the closest point to the current one
    :rtype tuple(float, float):
    """

    try:
        dist_1 = distance_formula(current_x, current_y, p1_x, p1_y)
    except TypeError:
        return p2_x, p2_y

    try:
        dist_2 = distance_formula(current_x, current_y, p2_x, p2_y)
    except TypeError:
        return p1_x, p1_y

    if dist_1 < dist_2:
        return p1_x, p1_y
    else:
        return p2_x, p2_y
