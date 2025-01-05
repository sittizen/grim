from grim.character import Character
from grim.character.stats import Attribute, Save


def test_char_creation() -> None:
    char = Character.create()
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
        assert char.saves[save][1] == 0

    # assert char.is_complete is False
