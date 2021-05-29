import math


class LevelMap:
    """
    Data class for holding information directly related to the map for the present level.
    """

    default_squares_x = 16
    default_squares_y = 16

    def __init__(self,
                 map_str: str,
                 map_squares_x: int = default_squares_x,
                 map_squares_y: int = default_squares_y
                 ):
        """
        Sets up a level Map with a grid coordinate system for locating objects easily.
        """

        assert (len(map_str) == map_squares_x * map_squares_y)

        self.map_str = map_str
        self.map_squares_x = map_squares_x
        self.map_squares_y = map_squares_y

    def get_symbol_at_map_xy(self, x: float, y: float) -> str:
        """
        Get the map symbol at the map coordinate
        """
        map_index = math.floor(x) + math.floor(y) * self.map_squares_x
        return self.map_str[map_index]
