import abc


class Components(metaclass=abc.ABCMeta):
    """
    Interface class for UI Components
    """
    @abc.abstractmethod
    def get_height(self):
        """
        Gets the height of the component
        :return:
        """
        pass

    @abc.abstractmethod
    def get_width(self):
        """
        Gets the width of the component
        :return:
        """
        pass
