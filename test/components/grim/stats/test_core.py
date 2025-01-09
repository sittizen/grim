from enum import StrEnum

from grim.stats import Stats


class Attributes(StrEnum):
    STR = "Strength"
    INT = "Intelligence"


class Saves(StrEnum):
    PA = "Paralysis"
    PO = "Poison"


def test_stat_group() -> None:
    attributes = Stats(Attributes)
    assert attributes.STR == 0
    assert attributes.INT == 0

    attributes.STR = 10  # type: ignore
    assert attributes.STR == 10

    saves = Stats(Saves)
    saves.PA = 1  # type: ignore
    assert saves.PA == 1


def test_tweak() -> None:
    attributes = Stats(Attributes)
    attributes.STR = 10  # type: ignore
    attributes.INT = 10  # type: ignore

    attributes.tweak("fighter", Attributes.STR, 1)
    attributes.tweak("mage", Attributes.INT, 1)

    attributes.apply("fighter")
    assert attributes.STR == 11
    assert attributes.INT == 10

    attributes.remove("fighter")
    attributes.apply("mage")
    assert attributes.STR == 10
    assert attributes.INT == 11

    attributes.apply("fighter")
    assert attributes.STR == 11
    assert attributes.INT == 11

    assert attributes.layers == {"fighter", "mage"}
    attributes.remove("mage")
    attributes.remove("fighter")
    assert attributes.layers == set()
