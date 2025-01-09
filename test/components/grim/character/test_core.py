# import pytest
from grim.character import Character

from grim.character.races import Human
from grim.character.stats import Attributes, Saves


def test_d6_down_the_line() -> None:
    char = Character.roll()
    for attribute in Attributes:
        assert 6 <= getattr(char.attributes, attribute.name) <= 15

    for save in Saves:
        assert getattr(char.saves, save.name) == 0

    assert char.race is None


#    with pytest.raises(ValueError, match="Missing class"):
#        char.is_complete


def test_attributes_swap() -> None:
    char = Character.roll()
    old_str = char.attributes.STR
    old_kno = char.attributes.KNO
    char.swap(Attributes.STR, Attributes.KNO)
    assert char.attributes.STR == old_kno
    assert char.attributes.KNO == old_str


def test_race_choice() -> None:
    char = Character.roll()
    char.apply_race(Human)
    assert isinstance(char.race, Human)


# def test_main_class_char_creation() -> None:
#    char = Character.roll(class_=Fighter)
#    assert char.main_attribute in (Attribute.STR, Attribute.DEX)
#    for attribute in (
#        Attribute.STR,
#        Attribute.DEX,
#        Attribute.CON,
#        Attribute.KNO,
#        Attribute.PER,
#        Attribute.CHA,
#        Attribute.ACC,
#    ):
#        assert 6 <= char.attributes[attribute] <= 15
#        assert char.attributes[char.main_attribute] >= char.attributes[attribute]

#    assert char.saves[Save.PA].val == 1
#    assert char.saves[Save.MFX].val == -1
