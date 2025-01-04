from enum import Enum
from hashlib import md5


class Attribute:
    name: Enum
    value: int

    def __init__(self, name: Enum, value: int):
        self.name = name
        self.value = value


class Save:
    name: str
    value: int
    on_attribute: Attribute

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value


class Modifier:
    stat: Enum
    val: int

    def __init__(self, stat: Enum, val: int):
        self.stat = stat
        self.val = val

    @property
    def uid(self) -> str:
        return md5(f"{self.stat.name}{self.val}".encode()).hexdigest()
