from grim.dice import d
from grim.stats import Stats

from .layers.classes import Class
from .layers.races import Race
from .stats import Attributes, Saves


class Character:
    def __init__(self) -> None:
        self.class_: Class | None = None
        self.race: Race | None = None
        self.attributes = Stats(Attributes)
        for attr in Attributes:
            setattr(self.attributes, attr.name, d(6, 6, 6, capl=2, caph=5))
        self.saves = Stats(Saves)
        for save in Saves:
            setattr(self.saves, save.name, 0)

    def __repr__(self) -> str:
        out = {"class": self.class_, "attributes": self.attributes, "saves": self.saves}
        return str(out)

    @staticmethod
    def roll() -> "Character":
        return Character()

    def check_complete(self) -> dict[str, bool]:
        return {
            "race": self.race is not None,
            "class": self.class_ is not None,
        }

    def swap(self, a: Attributes, b: Attributes) -> None:
        b_ = getattr(self.attributes, b.name)
        setattr(self.attributes, b.name, getattr(self.attributes, a.name))
        setattr(self.attributes, a.name, b_)

    def lay_race(self, race: type[Race]) -> None:
        self.race = race()

    def lay_class(self, class_: type[Class]) -> None:
        self.class_ = class_()
        for tweak in self.class_.tweaks.values():
            if len(tweak) == 1:
                stat, val = tweak[0][0], tweak[0][1]
                if isinstance(stat, Attributes):
                    self.attributes.tweak(class_.name, stat, val)
                if isinstance(stat, Saves):
                    self.saves.tweak(class_.name, stat, val)

        self.attributes.apply(class_.name)
        self.saves.apply(class_.name)
