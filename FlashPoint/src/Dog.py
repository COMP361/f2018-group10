from src.Animal import Animal


class Dog(Animal):

    def __init__(self, name, age):
        Animal.__init__(self, name, age)

    @staticmethod
    def bark():
        print("BARK")
