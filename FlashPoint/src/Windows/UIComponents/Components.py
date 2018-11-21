import abc


class Components(metaclass=abc.ABCMeta):
    """
    Abstract class for UI Components
    """
    def __init__(self, x: int, y: int, width: int, height: int):
        self._height = height
        self._width = width
        self._x = x
        self._y = y

    @property
    def height(self):
        """
        Gets the height of the component
        :return: int
        """
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def width(self):
        """
        Gets the width of the component
        :return: int
        """
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @abc.abstractmethod
    def change_pos(self, x: int, y: int):
        """
        Changes the position of the component
        :return:
        """
        pass

    @property
    def x(self):
        """
        Gets the X coordinates of the component
        :return: int
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        """
        Gets the Y coordinates of the component
        :return: int
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
