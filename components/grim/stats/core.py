class Attribute:
    name: str
    value: int

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value


class Save:
    name: str
    value: int
    on_attribute: Attribute

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
