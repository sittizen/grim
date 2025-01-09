from grim.stats import Stats

from .classes import Class
from .stats import Attribute, Save


class Character:
    def __init__(self, **kwargs: Attribute | Save | type[Class]):
        for val in kwargs.values():
            if isinstance(val, Attribute):
                self.attributes = Stats(Attribute)
            if isinstance(val, Save):
                self.saves = Stats(Save)
            if isinstance(val, Class):
                self.class_ = val

    def __repr__(self) -> str:
        out = {
            "class": self.class_,  # type: ignore
            "attributes": self.attributes,
            "saves": self.saves,
        }
        return str(out)

    # def _apply_class(self, class_: type[Class], attrs: list[Attribute], vals: list[int]) -> None:
    #    self.class_ = class_
    #    shuffle(class_.main_attr)
    #    self.main_attribute = class_.main_attr[0]
    #    attrs.remove(class_.main_attr[0])
    #    self.attributes[class_.main_attr[0]] = vals[0]
    #    vals.pop(0)
    #    for tweak in class_.tweaks:
    #        choice = tweak.choose()
    #        if choice is not None:
    #            if choice.cat == Save:
    #                self.saves[cast(Save, choice.stat)].val += choice.val

    # @property
    # def is_complete(self) -> None:
    #    if self.class_ is None:
    #        raise ValueError("Missing class")

    # @staticmethod
    # def roll(class_: type[Class] | None = None) -> "Character":
    #    out = Character(
    #        poison=SaveVal(Save.PO, 0, Attribute.CON),
    #        paralysis=SaveVal(Save.PA, 0, Attribute.STR),
    #        aoe=SaveVal(Save.AOE, 0, Attribute.DEX),
    #        mfx=SaveVal(Save.MFX, 0, Attribute.PER),
    #    )

    #    vals = sorted([d(6, 6, 6, capl=2, caph=5) for _ in range(7)], reverse=True)
    #    attrs = [
    #        Attribute.STR,
    #        Attribute.DEX,
    #        Attribute.CON,
    #        Attribute.KNO,
    #        Attribute.PER,
    #        Attribute.CHA,
    #        Attribute.ACC,
    #    ]
    #    shuffle(attrs)

    #    if class_ is not None:
    #        out._apply_class(class_, attrs, vals)

    #    for count, attr in enumerate(attrs):
    #        out.attributes[attr] = vals[count]

    #    return out
