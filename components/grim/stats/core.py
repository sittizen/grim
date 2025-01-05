from enum import Enum
from hashlib import md5


class StatVal:
    """A stat is choosen among the names of a particular StrEnum and has a value."""

    name: Enum
    value: int


class AttributeVal(StatVal):
    """An attribute represents an absolute measure of some trait."""

    def __init__(self, name: Enum, value: int):
        self.name = name
        self.value = value


class SaveVal(StatVal):
    """A save represents the ability to respond to some specific threat, modifying the check against an attribute."""

    on_attribute: Enum

    def __init__(self, name: Enum, value: int, on_attribute: Enum):
        self.name = name
        self.value = value
        self.on_attribute = on_attribute


class Tweak:
    """A tweak can be applied to rolled value of Stats when building a character."""

    cat: type[Enum]
    stat: Enum
    val: int

    def __init__(self, cat: type[Enum], stat: Enum, val: int):
        self.cat = cat
        self.stat = stat
        self.val = val

    @property
    def uid(self) -> str:
        return md5(f"{str(self.cat)}{self.stat}{self.val}".encode()).hexdigest()
