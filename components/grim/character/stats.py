from enum import Enum


class Attribute(Enum):
    STR = "Strength"
    DEX = "Dexterity"
    CON = "Constitution"
    KNO = "Knowledge"
    PER = "Perception"
    CHA = "Charisma"
    ACC = "Accuracy"


class Save(Enum):
    PA = "Paralysis"
    AOE = "Area of Effect"
    PO = "Poison"
    MFX = "Magic Effect"
