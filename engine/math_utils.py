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


def get_closest_point(current_coord, poi_1, poi_2):
    """
    Given a current position and two other positions which we're interested in, works out which of the two is
    closest to the current position

    :param tuple(float, float) current_coord:
    :param tuple(float, float) poi_1: Coordinate of a POI. May be partial (e.g. either value None)
    :param tuple(float, float) poi_2: Coordinate of a POI. May be partial (e.g. either value None)
    :return: the closest point to the current one
    :rtype tuple(float, float):
    """

    # if we found two potential points of interest, which is closer to the origin?
    if poi_1[0] and poi_1[1] and poi_2[0] and poi_2[1]:
        dist_1 = distance_formula(current_coord, poi_1)
        dist_2 = distance_formula(current_coord, poi_2)

        if dist_1 < dist_2:
            return poi_1
        else:
            return poi_2

    # else we only have 1 point to chose from anyway...
    elif poi_1[0] and poi_1[1]:
        return poi_1

    else:
        return poi_2