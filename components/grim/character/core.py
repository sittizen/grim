from enum import Enum

from grim.dice import d
from grim.stats import Stats

from .layers import Layer
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

    def lay(self, layer: type[Layer]) -> None:
        obj = layer()
        if issubclass(layer, Class):
            if self.class_ is not None:
                raise ValueError(f"{layer} already chosen")
            self.class_ = obj  # type: ignore
        elif issubclass(layer, Race):
            if self.race is not None:
                raise ValueError(f"{layer} already chosen")
            self.race = obj  # type: ignore
        else:
            raise ValueError("Invalid Layer type")

        for choice in obj.layer.values():
            stat, val = list(choice.items())[0]
            if isinstance(stat, Attributes):
                self.attributes.tweak(layer.name, stat, val)
            if isinstance(stat, Saves):
                self.saves.tweak(layer.name, stat, val)

        self.attributes.apply(layer.name)
        self.saves.apply(layer.name)

    def race_choose(self, tweak: str, choice: Enum) -> None:
        if self.race is None:
            raise ValueError("No class to choose for")
        self.race.choose(tweak, choice)
        if isinstance(choice, Attributes):
            self.attributes.tweak(self.race.name, choice, self.race.layer[tweak][choice])

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
