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
                raise ValueError("Class already chosen")
            self.class_ = obj  # type: ignore
        elif issubclass(layer, Race):
            if self.race is not None:
                raise ValueError("Race already chosen")
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

    def choose(self, layer: type[Layer], tweak: str, choice: Enum) -> None:
        obj: Layer
        if issubclass(layer, Class):
            if self.class_ is None:
                raise ValueError(f"No {layer} to choose for")
            obj = self.class_
        elif issubclass(layer, Race):
            if self.race is None:
                raise ValueError(f"No {layer} to choose for")
            obj = self.race
        else:
            raise ValueError("Invalid Layer type")

        obj.choose(tweak, choice)
        if isinstance(choice, Attributes):
            self.attributes.tweak(obj.name, choice, obj.layer[tweak][choice])

    def remove(self, layer: type[Layer]) -> None:
        obj: Layer | None
        if issubclass(layer, Class):
            if self.class_ is None:
                return
            obj = self.class_
            self.class_ = None
        elif issubclass(layer, Race):
            if self.race is None:
                return
            obj = self.race
            self.race = None
        else:
            raise ValueError("Invalid Layer type")

        # todo, when removing Class or Race the name must be found
        self.attributes.remove(obj.name)
        self.saves.remove(obj.name)
