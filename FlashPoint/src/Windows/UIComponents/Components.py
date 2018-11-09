import abc


class Components(metaclass=abc.ABCMeta):
    """
    Interface class for UI Components
    """
    def __init__(self):
        self.height = None
        self.width = None
        self.x = None
        self.y = None

    @property
    def height(self):
        """
        Gets the height of the component
        :return: int
        """
        return self.height

    @height.setter
    def height(self, height: int):
        self.height = height

    @property
    def width(self):
        """
        Gets the width of the component
        :return: int
        """
        return self.width

    @width.setter
    def width(self, width):
        self.width = width

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
        return self.x

    @x.setter
    def x(self, x):
        self.x = x

    @property
    def y(self):
        """
        Gets the Y coordinates of the component
        :return: int
        """
        return self.y

    @y.setter
    def y(self, y):
        self.y = y
