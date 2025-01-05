import pytest
from grim.character import Character
from grim.character.classes import Fighter
from grim.character.stats import Attribute, Save


def test_bare_char_creation() -> None:
    char = Character.roll()
    for attribute in (
        Attribute.STR,
        Attribute.DEX,
        Attribute.CON,
        Attribute.KNO,
        Attribute.PER,
        Attribute.CHA,
        Attribute.ACC,
    ):
        assert 6 <= char.attributes[attribute] <= 15

    for save in (Save.PA, Save.PO, Save.AOE, Save.MFX):
        assert char.saves[save].val == 0

    with pytest.raises(ValueError, match="Missing class"):
        char.is_complete


def test_main_class_char_creation() -> None:
    char = Character.roll(class_=Fighter)
    assert char.main_attribute in (Attribute.STR, Attribute.DEX)
    for attribute in (
        Attribute.STR,
        Attribute.DEX,
        Attribute.CON,
        Attribute.KNO,
        Attribute.PER,
        Attribute.CHA,
        Attribute.ACC,
    ):
        assert 6 <= char.attributes[attribute] <= 15
        assert char.attributes[char.main_attribute] >= char.attributes[attribute]

    assert char.saves[Save.PA].val == 1
    assert char.saves[Save.MFX].val == -1
