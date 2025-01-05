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

    def _apply_class(self, class_: type[Class]) -> None:
        for vals in class_.tweaks.values():
            for val in vals:
                if len(val) == 1:
                    if val[0].cat == Save:
                        self.saves[cast(Save, val[0].stat)].val += val[0].val

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
            out.class_ = class_
            shuffle(class_.main_attr)
            out.main_attribute = class_.main_attr[0]
            attrs.remove(class_.main_attr[0])
            out.attributes[class_.main_attr[0]] = vals[0]
            vals.pop(0)

            out._apply_class(class_)

        for count, attr in enumerate(attrs):
            out.attributes[attr] = vals[count]

        return out
