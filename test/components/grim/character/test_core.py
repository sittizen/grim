from grim.character import Character


def test_char_creation() -> None:
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

    # assert char.is_complete is False
