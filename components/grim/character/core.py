from typing import cast

from grim.dice import d
from grim.stats import AttributeVal, SaveVal

from .stats import Attribute, Save


class Character:
    attributes: dict[Attribute, int] = {}
    saves: dict[Save, tuple[Attribute, int]] = {}

    def __init__(self, **kwargs: AttributeVal | SaveVal):
        for val in kwargs.values():
            if isinstance(val, AttributeVal):
                self.attributes[cast(Attribute, val.name)] = val.value
            if isinstance(val, SaveVal):
                self.saves[cast(Save, val.name)] = (cast(Attribute, val.on_attribute), val.value)

    @staticmethod
    def create() -> "Character":
        strenght = AttributeVal(Attribute.STR, d((6, 6, 6), capl=2, caph=5))
        dexterity = AttributeVal(Attribute.DEX, d((6, 6, 6), capl=2, caph=5))
        constitution = AttributeVal(Attribute.CON, d((6, 6, 6), capl=2, caph=5))
        knowledge = AttributeVal(Attribute.KNO, d((6, 6, 6), capl=2, caph=5))
        perception = AttributeVal(Attribute.PER, d((6, 6, 6), capl=2, caph=5))
        charisma = AttributeVal(Attribute.CHA, d((6, 6, 6), capl=2, caph=5))
        accuracy = AttributeVal(Attribute.ACC, d((6, 6, 6), capl=2, caph=5))
        return Character(
            strenght=strenght,
            dexterity=dexterity,
            constitution=constitution,
            knowledge=knowledge,
            perception=perception,
            charisma=charisma,
            accuracy=accuracy,
            poison=SaveVal(Save.PO, 0, Attribute.CON),
            paralysis=SaveVal(Save.PA, 0, Attribute.STR),
            aoe=SaveVal(Save.AOE, 0, Attribute.DEX),
            mfx=SaveVal(Save.MFX, 0, Attribute.PER),
        )
