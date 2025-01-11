from grim.dice import d
from grim.stats import Stats

from .classes import Class
from .races import Race
from .stats import Attributes, Saves


class Character:
    def __init__(
        self,
    ) -> None:
        self.class_: Class | None = None
        self.race: Race | None = None
        self.attributes = Stats(Attributes)
        for attr in Attributes:
            setattr(self.attributes, attr.name, d(6, 6, 6, capl=2, caph=5))
        self.saves = Stats(Saves)
        for save in Saves:
            setattr(self.saves, save.name, 0)

    def __repr__(
        self,
    ) -> str:
        out = {
            "class": self.class_,
            "attributes": self.attributes,
            "saves": self.saves,
        }
        return str(out)

    def swap(
        self,
        a: Attributes,
        b: Attributes,
    ) -> None:
        b_ = getattr(
            self.attributes,
            b.name,
        )
        setattr(
            self.attributes,
            b.name,
            getattr(
                self.attributes,
                a.name,
            ),
        )
        setattr(
            self.attributes,
            a.name,
            b_,
        )

    @property
    def is_complete(
        self,
    ) -> None:
        if self.race is None:
            raise ValueError("Missing race")
        if self.class_ is None:
            raise ValueError("Missing class")

    @staticmethod
    def roll() -> "Character":
        return Character()

    def apply_race(
        self,
        race: type[Race],
    ) -> None:
        self.race = race()

    def apply_class(
        self,
        class_: type[Class],
    ) -> None:
        self.class_ = class_()
