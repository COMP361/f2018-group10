import abc


class Components(metaclass=abc.ABCMeta):
    """
    Interface class for UI Components
    """
    @abc.abstractmethod
    def get_height(self):
        """
        Gets the height of the component
        :return: int
        """
        pass

    @abc.abstractmethod
    def get_width(self):
        """
        Gets the width of the component
        :return: int
        """
        pass

    def change_pos(self, x: int, y: int):
        """
        Changes the position of the component
        :return:
        """
        pass

    def get_x(self):
        """
        Gets the X coordinates of the component
        :return: int
        """
        pass

    def get_y(self):
        """
        Gets the Y coordinates of the component
        :return: int
        """
        pass
