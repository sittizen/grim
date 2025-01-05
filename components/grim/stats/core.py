from enum import StrEnum
from hashlib import md5


class Stat:
    """A stat is choosen among the names of a particular StrEnum and has a value."""

    name: StrEnum
    value: int


class Attribute(Stat):
    """An attribute represents an absolute measure of some trait."""

    def __init__(self, name: StrEnum, value: int):
        self.name = name
        self.value = value


class Save(Stat):
    """A save represents the ability to respond to some specific threat, modifying the check against an attribute."""

    on_attribute: Attribute

    def __init__(self, name: StrEnum, value: int, on_attribute: Attribute):
        self.name = name
        self.value = value
        self.on_attribute = on_attribute


class Tweak:
    """A tweak can be applied to rolled value of Stats when building a character."""

    cat: type[StrEnum]
    stat: StrEnum
    val: int

    def __init__(self, cat: type[StrEnum], stat: StrEnum, val: int):
        self.cat = cat
        self.stat = stat
        self.val = val

    @property
    def uid(self) -> str:
        return md5(f"{str(self.cat)}{self.stat}{self.val}".encode()).hexdigest()
