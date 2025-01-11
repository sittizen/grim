from grim.character import Character
from grim.character.layers.classes import Fighter
from grim.character.layers.races import Human
from grim.character.stats import Attributes, Saves


def test_d6_down_the_line() -> None:
    char = Character.roll()
    for attribute in Attributes:
        assert 6 <= getattr(char.attributes, attribute.name)
        assert getattr(char.attributes, attribute.name) <= 15

    for save in Saves:
        assert getattr(char.saves, save.name) == 0

    assert char.check_complete() == {
        "race": False,
        "class": False,
    }


def test_attributes_swap() -> None:
    char = Character.roll()
    old_str = char.attributes.STR
    old_kno = char.attributes.KNO
    char.swap(Attributes.STR, Attributes.KNO)
    assert char.attributes.STR == old_kno
    assert char.attributes.KNO == old_str


def test_race_choice() -> None:
    char = Character.roll()
    char.lay_race(Human)
    assert isinstance(char.race, Human)


def test_class_choice() -> None:
    char = Character.roll()
    char.lay_class(Fighter)
    assert char.check_complete() == {
        "race": False,
        "class": True,
    }

    assert char.saves.PA == 1
    assert char.saves.MFX == -1
