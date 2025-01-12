from enum import Enum

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
            "class": self.class_ is not None and self.class_.has_pending_choices is False,
        }

    def swap(self, a: Attributes, b: Attributes) -> None:
        b_ = getattr(self.attributes, b.name)
        setattr(self.attributes, b.name, getattr(self.attributes, a.name))
        setattr(self.attributes, a.name, b_)

    def lay_race(self, race: type[Race]) -> None:
        self.race = race()

    def lay_class(self, class_: type[Class]) -> None:
        if self.class_ is not None:
            raise ValueError("Class already chosen")
        self.class_ = class_()
        for choice in self.class_.layer.values():
            stat, val = list(choice.items())[0]
            if isinstance(stat, Attributes):
                self.attributes.tweak(class_.name, stat, val)
            if isinstance(stat, Saves):
                self.saves.tweak(class_.name, stat, val)

        self.attributes.apply(class_.name)
        self.saves.apply(class_.name)

    def class_choose(self, tweak: str, choice: Enum) -> None:
        if self.class_ is None:
            raise ValueError("No class to choose for")
        self.class_.choose(tweak, choice)
        if isinstance(choice, Attributes):
            self.attributes.tweak(self.class_.name, choice, self.class_.layer[tweak][choice])

    def remove_class(self) -> None:
        if self.class_ is None:
            raise ValueError("No class to remove")
        self.attributes.remove(self.class_.name)
        self.saves.remove(self.class_.name)
        self.class_ = None
