import math
from typing import Union, Tuple


def distance_formula(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Distance between two points is defined as the square root of (x2 - x1)^2 + (y2 - y1) ^ 2

    :raises TypeError: Any of the values are non-numeric or None.
    """
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def gradient(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Find the gradient of a line between two coordinates
    """
    return (y2 - y1) / (x2 - x1)


def get_y_for_x(x: float, gradient: float, y_intercept: float) -> float:
    """
    Linear equation, y = mx + c
    """
    return (x * gradient) + y_intercept


def get_x_for_y(y: float, gradient: float, y_intercept: float):
    """
    Linear equation reorganised, x = (y - c) / m
    """
    return (y - y_intercept) / gradient


def get_closest_point(
        current_x: float,
        current_y: float,
        p1_x: Union[float, None],
        p1_y: Union[float, None],
        p2_x: Union[float, None],
        p2_y: Union[float, None]
) -> Tuple[float, float]:
    """
    Given a current position and two other positions which we're interested in, works out which of the two is
    closest to the current position.

    If 1 of the POIs is partial (contains a None), the other will be returned. If both are None, the second POI will
    be returned, but this behavior should be considered undefined.

    :return: the closest point to the current one
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


def get_next_x_poi(
        origin_x: float,
        ray_x: float,
        gradient: float,
        intercept: float,
        x_increasing: bool,
        x_whole: bool
) -> Tuple[Union[float, None], Union[float, None]]:
    """
    Finds the next x Point of Interest on this line. I.e. the coordinate where the ray defined by the parameters
    will be a whole x value.

    e.g. If the current ray is at x=1, y=1.5 and we know that x is increasing, the next whole x will be 2, and we
    will need to user the gradient and intercept to calculate y at this location.

    If the line is vertical (i.e. x doesn't change) then there will not be another x POI.
    """

    if ray_x == origin_x:  # vertical line. Y varies but not x
        return None, None

    if x_increasing:
        if x_whole:
            next_whole_x = ray_x + 1
        else:
            next_whole_x = math.ceil(ray_x)

    else:
        if x_whole:
            next_whole_x = ray_x - 1
        else:
            next_whole_x = math.floor(ray_x)

    y_at_next_whole_x = get_y_for_x(next_whole_x, gradient, intercept)

    return next_whole_x, y_at_next_whole_x


def get_next_y_poi(
        origin_x: float,
        origin_y: float,
        ray_y: float,
        gradient: float,
        intercept: float,
        y_increasing: bool,
        y_whole: bool
) -> Tuple[Union[float, None], Union[float, None]]:
    """
    Finds the next y Point of Interest on this line. I.e. the coordinate where the ray defined by the parameters
    will be a whole y value.

    Works similarly to the next_x poi, but if the line is horizontal (i.e. y doesn't change) there will be no next
    y POI.

    This requires an additional parameter to next_x_poi, because in the case that the line is vertical, there will
    be a next y poi, but we won't have a gradient or intercept because the line is vertical, so we need the origin_x
    to set the x value.

    :return: coordinate
    """

    if ray_y == origin_y:  # horizontal line. x varies but not y
        return None, None

    if y_increasing:
        if y_whole:
            next_whole_y = ray_y + 1
        else:
            next_whole_y = math.ceil(ray_y)

    else:
        if y_whole:
            next_whole_y = ray_y - 1
        else:
            next_whole_y = math.floor(ray_y)

    if gradient:
        x_at_next_whole_y = get_x_for_y(next_whole_y, gradient, intercept)
    else:  # vertical line, y changes but x is the same as origin
        x_at_next_whole_y = origin_x

    return x_at_next_whole_y, next_whole_y


def get_new_coordinates(curr_x: float, curr_y: float, angle: float, speed: float):
    """
    Works out the next x, y coordinate given the current coordinate, an angle (from the x axis) and the speed
    (i.e distance of travel).

    :param curr_x:
    :param curr_y:
    :param angle:
    :param speed:
    :return: coordinate
    """
    new_x = curr_x + speed * math.cos(angle)
    new_y = curr_y + speed * math.sin(angle)
    return new_x, new_y