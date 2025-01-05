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


class TweakChoice:
    """For every list in the tuple, only one tweak can be chosen."""

    name: str
    choices: dict[str, dict[str, Tweak]] = {}

    def __init__(self, name: str, choices: dict[str, tuple[list[Tweak], ...]]):
        self.name = name
        for k, v in choices.items():
            self.choices[k] = {}
            for tweaks in v:
                for tweak in tweaks:
                    self.choices[k][tweak.uid] = tweak

    def choose(self, desc: str, uid: str) -> Tweak:
        choices = self.choices[desc]
        if uid in choices:
            return choices.pop(uid)
        raise ValueError(f"No such choice in {desc}")

    def done(self) -> bool:
        return all([len(x) == 0 for x in self.choices])
