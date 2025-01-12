import pytest
from grim.character import Character
from grim.character.layers.classes import Cleric, Fighter
from grim.character.layers.races import Elf
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


def test_layers() -> None:
    fighter = Fighter()

    assert fighter.name == "fighter"
    assert fighter.layer == {
        "save_pa": {Saves.PA: 1},
        "save_mfx": {Saves.MFX: -1},
    }
    assert fighter.has_pending_choices is True
    assert fighter.pending_choices == {
        "main_attribute": [(Attributes.STR, 1), (Attributes.DEX, 1)],
    }

    fighter.choose("main_attribute", Attributes.STR)

    assert fighter.has_pending_choices is False
    assert fighter.layer == {
        "main_attribute": {Attributes.STR: 1},
        "save_pa": {Saves.PA: 1},
        "save_mfx": {Saves.MFX: -1},
    }


def test_class_choice() -> None:
    char = Character.roll()
    char.lay(Fighter)
    base_dex = int(char.attributes.DEX)

    assert char.check_complete() == {
        "race": False,
        "class": False,  # still missing choices
    }

    char.class_choose("main_attribute", Attributes.DEX)
    assert char.check_complete()["class"] is True

    assert char.saves.PA == 1
    assert char.saves.MFX == -1
    assert char.attributes.DEX == base_dex + 1

    with pytest.raises(ValueError):
        char.lay(Cleric)

    char.remove_class()

    assert char.check_complete()["class"] is False

    assert char.saves.PA == 0
    assert char.saves.MFX == 0
    assert char.attributes.DEX == base_dex


def test_class_and_race_sum_layers() -> None:
    char = Character.roll()
    base_dex = int(char.attributes.DEX)

    char.lay(Fighter)
    char.class_choose("main_attribute", Attributes.DEX)
    assert char.attributes.DEX == base_dex + 1

    char.lay(Elf)
    char.race_choose("main_attribute", Attributes.DEX)

    assert char.attributes.DEX == base_dex + 2
