from enum import Enum
from typing import cast

from grim.dice import d
from grim.stats import Attribute, Modifier


class AttributeName(Enum):
    STR = "Strength"
    DEX = "Dexterity"
    CON = "Constitution"
    KNO = "Knowledge"
    PER = "Perception"
    CHA = "Charisma"
    ACC = "Accuracy"


class SaveName(Enum):
    PA = "Paralysis"
    AOE = "Area of Effect"
    PO = "Poison"
    MFX = "Magic Effect"


class RaceName(Enum):
    HUMAN = "Human"
    ELF = "Elf"
    DWARF = "Dwarf"
    ORC = "Orc"
    GOBLIN = "Goblin"
    KOBOLD = "Kobold"
    HALFLING = "Halfling"
    FAE = "Fae"
    BOGGART = "Boggart"


class ClassName(Enum):
    FIGHTER = "Fighter"
    ROGUE = "Rogue"
    WIZARD = "Wizard"
    CLERIC = "Cleric"


class SubClassName(Enum):
    KNIGHT = "Paladin"
    BARBARIAN = "Barbarian"
    RANGER = "Ranger"


class CharacterClass:
    main_class: ClassName
    sub_class: SubClassName

    def __init__(self, main_class: ClassName, sub_class: SubClassName):
        self.main_class = main_class
        self.sub_class = sub_class


class ClassModifiers:
    main_class: ClassName
    options: dict[str, tuple[Modifier, ...]]

    @property
    def pending(self) -> bool:
        return len(self.options.keys()) == 0

    def choose(self, choice_key: str, choice_val: Modifier) -> None:
        if choice_key not in self.options:
            raise ValueError(f"Invalid option: {choice_key}")
        if choice_val not in self.options[choice_key]:
            raise ValueError(f"Invalid choice: {choice_val}")
        setattr(self, choice_key, choice_val)
        del self.options[choice_key]


class Character:
    strenght: Attribute
    dexterity: Attribute
    constitution: Attribute
    knowledge: Attribute
    perceptione: Attribute
    charisma: Attribute
    accuracy: Attribute

    class_: CharacterClass

    def __init__(self, **kwargs: Attribute | ClassName | SubClassName):
        class_ = None
        subclass = None
        for key, value in kwargs.items():
            match key:
                case "class_":
                    class_ = value
                case "subclass":
                    subclass = value
                case _:
                    setattr(self, key, value)
        self.class_ = CharacterClass(main_class=cast(ClassName, class_), sub_class=cast(SubClassName, subclass))

    @staticmethod
    def create() -> "Character":
        return Character(
            strenght=Attribute(AttributeName.STR, d((6, 6, 6), capl=2, caph=5)),
            dexterity=Attribute(AttributeName.DEX, d((6, 6, 6), capl=2, caph=5)),
            constitution=Attribute(AttributeName.CON, d((6, 6, 6), capl=2, caph=5)),
            knowledge=Attribute(AttributeName.KNO, d((6, 6, 6), capl=2, caph=5)),
            perceptione=Attribute(AttributeName.PER, d((6, 6, 6), capl=2, caph=5)),
            charisma=Attribute(AttributeName.CHA, d((6, 6, 6), capl=2, caph=5)),
            accuracy=Attribute(AttributeName.ACC, d((6, 6, 6), capl=2, caph=5)),
        )
