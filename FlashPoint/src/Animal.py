class Animal:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def move(self,distance):
        print("The " + self.name + " has moved " + str(distance))
        return distance

