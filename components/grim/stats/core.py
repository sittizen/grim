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

    def __init__(self, stat: Enum, val: int):
        self.cat = type(stat)
        self.stat = stat
        self.val = val

    @property
    def uid(self) -> str:
        return md5(f"{str(self.cat)}{self.stat}{self.val}".encode()).hexdigest()


class TweakChoice:
    """For every list in the tuple, only one tweak can be chosen."""

    name: str
    choices: dict[str, Tweak] = {}
    _chosen: bool = False

    def __init__(self, name: str, choices: tuple[Tweak, ...]):
        self.name = name
        for tweak in choices:
            self.choices[tweak.uid] = tweak

    @property
    def done(self) -> bool:
        return self._chosen

    def choose(self, uid: str) -> Tweak:
        if uid in self.choices:
            self._chosen = True
            return self.choices[uid]
        raise ValueError(f"No such choice in {self.name}")
