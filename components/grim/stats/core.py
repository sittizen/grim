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

    def __init__(self, stat: Enum, val: int):
        self.cat: type[Enum] = type(stat)
        self.stat: Enum = stat
        self.val: int = val

    def __repr__(self) -> str:
        return f"{self.stat}: {self.val}"

    @property
    def uid(self) -> str:
        return md5(f"{str(self.cat)}{self.stat}{self.val}".encode()).hexdigest()


class TweakChoice:
    """For every list in the tuple, only one tweak can be chosen."""

    def __init__(self, name: str, choices: tuple[Tweak, ...]):
        self.choices: dict[str, Tweak] = {}
        self._chosen: bool = False
        self.name: str = name
        for tweak in choices:
            self.choices[tweak.uid] = tweak

    def __repr__(self) -> str:
        return f"{self.name}: {len(self.choices)} choices"

    @property
    def done(self) -> bool:
        return self._chosen

    def choose(self, uid: str | None = None) -> Tweak | None:
        if uid is None:
            if len(self.choices) == 1:
                self._chosen = True
                return list(self.choices.values())[0]
            return None
        if uid in self.choices:
            self._chosen = True
            return self.choices[uid]
        raise ValueError(f"No such choice in {self.name}")
