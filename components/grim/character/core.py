from enum import StrEnum

from grim.dice import d
from grim.stats import Attribute as AttrVal


class Attribute(StrEnum):
    STR = "Strength"
    DEX = "Dexterity"
    CON = "Constitution"
    KNO = "Knowledge"
    PER = "Perception"
    CHA = "Charisma"
    ACC = "Accuracy"


class Save(StrEnum):
    PA = "Paralysis"
    AOE = "Area of Effect"
    PO = "Poison"
    MFX = "Magic Effect"


class Race(StrEnum):
    HUMAN = "Human"
    ELF = "Elf"
    DWARF = "Dwarf"
    ORC = "Orc"
    GOBLIN = "Goblin"
    KOBOLD = "Kobold"
    HALFLING = "Halfling"
    FAE = "Fae"
    BOGGART = "Boggart"


class Character:
    strenght: AttrVal
    dexterity: AttrVal
    constitution: AttrVal
    knowledge: AttrVal
    perception: AttrVal
    charisma: AttrVal
    accuracy: AttrVal

    def __init__(self, **kwargs: AttrVal):
        for key, value in kwargs.items():
            match key:
                case _:
                    setattr(self, key, value)

    @staticmethod
    def create() -> "Character":
        return Character(
            strenght=AttrVal(Attribute.STR, d((6, 6, 6), capl=2, caph=5)),
            dexterity=AttrVal(Attribute.DEX, d((6, 6, 6), capl=2, caph=5)),
            constitution=AttrVal(Attribute.CON, d((6, 6, 6), capl=2, caph=5)),
            knowledge=AttrVal(Attribute.KNO, d((6, 6, 6), capl=2, caph=5)),
            perceptione=AttrVal(Attribute.PER, d((6, 6, 6), capl=2, caph=5)),
            charisma=AttrVal(Attribute.CHA, d((6, 6, 6), capl=2, caph=5)),
            accuracy=AttrVal(Attribute.ACC, d((6, 6, 6), capl=2, caph=5)),
        )
