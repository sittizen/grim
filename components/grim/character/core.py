from dataclasses import dataclass
from random import shuffle
from typing import cast

from grim.dice import d
from grim.stats import AttributeVal, SaveVal

from .classes import Class
from .stats import Attribute, Save


@dataclass
class SaveTuple:
    attr: Attribute
    val: int


class Character:
    attributes: dict[Attribute, int] = {}
    saves: dict[Save, SaveTuple] = {}
    class_: type[Class] | None = None
    main_attribute: Attribute | None = None

    def __init__(self, **kwargs: AttributeVal | SaveVal | type[Class]):
        for val in kwargs.values():
            if isinstance(val, AttributeVal):
                self.attributes[cast(Attribute, val.name)] = val.value
            if isinstance(val, SaveVal):
                self.saves[cast(Save, val.name)] = SaveTuple(attr=cast(Attribute, val.on_attribute), val=val.value)
            if isinstance(val, Class):
                self.main_class = val

    def __repr__(self) -> str:
        out = {
            "class": self.class_,
            "main_attribute": self.main_attribute,
            "attributes": self.attributes,
            "saves": self.saves,
        }
        return str(out)

    def _apply_class(self, class_: type[Class], attrs: list[Attribute], vals: list[int]) -> None:
        self.class_ = class_
        shuffle(class_.main_attr)
        self.main_attribute = class_.main_attr[0]
        attrs.remove(class_.main_attr[0])
        self.attributes[class_.main_attr[0]] = vals[0]
        vals.pop(0)
        for tweak in class_.tweaks:
            choice = tweak.choose()
            if choice is not None:
                if choice.cat == Save:
                    self.saves[cast(Save, choice.stat)].val += choice.val

    @property
    def is_complete(self) -> None:
        if self.class_ is None:
            raise ValueError("Missing class")

    @staticmethod
    def roll(class_: type[Class] | None = None) -> "Character":
        out = Character(
            poison=SaveVal(Save.PO, 0, Attribute.CON),
            paralysis=SaveVal(Save.PA, 0, Attribute.STR),
            aoe=SaveVal(Save.AOE, 0, Attribute.DEX),
            mfx=SaveVal(Save.MFX, 0, Attribute.PER),
        )

        vals = sorted([d((6, 6, 6), capl=2, caph=5) for _ in range(7)], reverse=True)
        attrs = [
            Attribute.STR,
            Attribute.DEX,
            Attribute.CON,
            Attribute.KNO,
            Attribute.PER,
            Attribute.CHA,
            Attribute.ACC,
        ]
        shuffle(attrs)

        if class_ is not None:
            out._apply_class(class_, attrs, vals)

        for count, attr in enumerate(attrs):
            out.attributes[attr] = vals[count]

        return out
