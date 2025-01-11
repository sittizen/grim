# import pytest
from grim.character import (
    Character,
)
from grim.character.races import (
    Human,
)
from grim.character.stats import (
    Attributes,
    Saves,
)


def test_d6_down_the_line() -> None:
    char = Character.roll()
    for attribute in Attributes:
        assert 6 <= getattr(char.attributes, attribute.name)
        assert getattr(char.attributes, attribute.name) <= 15

    for save in Saves:
        assert getattr(char.saves, save.name) == 0
    assert char.race is None


def test_attributes_swap() -> None:
    char = Character.roll()
    old_str = char.attributes.STR
    old_kno = char.attributes.KNO
    char.swap(
        Attributes.STR,
        Attributes.KNO,
    )
    assert char.attributes.STR == old_kno
    assert char.attributes.KNO == old_str


def test_race_choice() -> None:
    char = Character.roll()
    char.apply_race(Human)
    assert isinstance(char.race, Human)
