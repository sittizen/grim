from enum import StrEnum

from grim.stats import Tweak, TweakChoice


class Attribute(StrEnum):
    STR = "Strength"
    DEX = "Dexterity"


class Save(StrEnum):
    PO = "Poison"


def test_tweaks() -> None:
    str1 = Tweak(stat=Attribute.STR, val=1)
    strm1 = Tweak(stat=Attribute.STR, val=-1)
    s1 = Tweak(stat=Save.PO, val=1)

    assert str1.uid != strm1.uid != s1.uid
    assert str1.cat == Attribute


def test_choice() -> None:
    str1 = Tweak(Attribute.STR, 1)
    dex1 = Tweak(Attribute.DEX, 1)
    choice = TweakChoice("str_or_dex", choices=(str1, dex1))

    assert choice.choices == {str1.uid: str1, dex1.uid: dex1}
    assert choice.done is False
    assert choice.choose(str1.uid) == str1
    assert choice.done is True


def test_single_choice() -> None:
    str1 = Tweak(Attribute.STR, 1)
    choice = TweakChoice("str+1", choices=(str1,))

    assert choice.done is False
    assert choice.choose() == str1
    assert choice.done is True


def test_no_single_choice() -> None:
    str1 = Tweak(Attribute.STR, 1)
    dex1 = Tweak(Attribute.DEX, 1)
    choice = TweakChoice("str_or_dex", choices=(str1, dex1))

    assert choice.done is False
    assert choice.choose() is None
    assert choice.done is False
