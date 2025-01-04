from enum import Enum

from grim.stats import Modifier


class AttributeName(Enum):
    STR = "Strength"
    DEX = "Dexterity"


class SaveName(Enum):
    PO = "Poison"


def test_modifiers() -> None:
    str1 = Modifier(stat=AttributeName.STR, val=1)
    strm1 = Modifier(stat=AttributeName.STR, val=-1)
    s1 = Modifier(stat=SaveName.PO, val=1)
    assert str1.uid != strm1.uid != s1.uid
