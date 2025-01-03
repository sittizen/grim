from enum import Enum
from grim.stats import Attribute
from grim.dice import d


class AttributeName(Enum):
    STR = "Strength"
    DEX = "Dexterity"
    CON = "Constitution"
    KNO = "Knowledge"
    PER = "Perception"
    CHA = "Charisma"
    ACC = "Accuracy"


class SaveName(Enum):
    PA = "Paralysis"
    AOE = "Area of Effect"
    PO = "Poison"
    MFX = "Magic Effect"


class Character:
    strenght: Attribute
    dexterity: Attribute
    constitution: Attribute
    knowledge: Attribute
    perceptione: Attribute
    charisma: Attribute
    accuracy: Attribute

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def create():
        return Character(
            strenght=Attribute(AttributeName.STR, d((6, 6, 6), capl=2, caph=5)),
            dexterity=Attribute(AttributeName.DEX, d((6, 6, 6), capl=2, caph=5)),
            constitution=Attribute(AttributeName.CON, d((6, 6, 6), capl=2, caph=5)),
            knowledge=Attribute(AttributeName.KNO, d((6, 6, 6), capl=2, caph=5)),
            perceptione=Attribute(AttributeName.PER, d((6, 6, 6), capl=2, caph=5)),
            charisma=Attribute(AttributeName.CHA, d((6, 6, 6), capl=2, caph=5)),
            accuracy=Attribute(AttributeName.ACC, d((6, 6, 6), capl=2, caph=5)),
        )
