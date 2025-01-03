from grim.character import Character
from grim.dice import d


def test_char_creation():
    char = Character.create()
    for attribute in (
        "strenght",
        "dexterity",
        "constitution",
        "knowledge",
        "perceptione",
        "charisma",
        "accuracy",
    ):
        assert 6 <= getattr(char, attribute).value <= 15

    assert char.is_complete is False
