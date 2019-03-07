class Abra():

    def __init__(self, name: str, age: int, gender: str):
        self._name = name
        self._age = age
        self._gender = gender


def main():
    d = {
        "Name": "Abhijay",
        "Age": 21,
        "Gender": "Male"
    }
    for key, value in d.items():
        print("Key:", key)
        print("Value:", value)


if __name__ == '__main__':
    main()
