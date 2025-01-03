from enum import Enum
from grim.stats import Attribute
from grim.dice import d


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


class AttributeModifier:
    attribute: AttributeName
    value: int

    def __init__(self, attribute: AttributeName, value: int):
        self.attribute = attribute
        self.value = value


class SaveModifier:
    save: SaveName
    value: int

    def __init__(self, save: SaveName, value: int):
        self.save = save
        self.value = value


class ClassModifiers:
    main_class: ClassName

    @staticmethod
    def get(class_: str):
        if class_ == ClassName.FIGHTER:
            return ClassModifiersFighter()
        raise ValueError(f"Invalid class: {class_}")

    @property
    def choices(self):
        return {}

    @property
    def pending(self):
        return len(self.choices().keys()) == 0

    def choose(self, choice_key, choice_val):
        if choice_key not in self.choices:
            raise ValueError(f"Invalid choice key: {choice_key}")
        if choice_val not in self.choices[choice_key]:
            raise ValueError(f"Invalid choice value: {choice_val}")
        setattr(self, choice_key, choice_val)
        del self.choices[choice_key]


class ClassModifiersFighter(ClassModifiers):
    def __init__(self):
        self.main_class = ClassName

    @property
    def choices(self):
        return {
            "attributes": (
                AttributeModifier(AttributeName.STR, 1),
                AttributeModifier(AttributeName.DEX, 1),
                AttributeModifier(AttributeName.CON, 1),
            ),
            "saves": (SaveModifier(SaveName.PA, 1),),
        }


class Character:
    strenght: Attribute
    dexterity: Attribute
    constitution: Attribute
    knowledge: Attribute
    perceptione: Attribute
    charisma: Attribute
    accuracy: Attribute

    class_ = CharacterClass

    _pending = []

    def __init__(self, **kwargs):
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
        self.class_ = CharacterClass(main_class=class_, sub_class=subclass)
        self._pending.append(ClassModifiers.get(class_))

    @staticmethod
    def create():
        return Character(
            strenght=Attribute(AttributeName.STR, d((6, 6, 6), capl=2, caph=5)),
            dexterity=Attribute(AttributeName.DEX, d((6, 6, 6), capl=2, caph=5)),
            constitution=Attribute(AttributeName.CON, d((6, 6, 6), capl=2, caph=5)),
            knowledge=Attribute(AttributeName.KNO, d((6, 6, 6), capl=2, caph=5)),
            perceptione=Attribute(AttributeName.PER, d((6, 6, 6), capl=2, caph=5)),
            charisma=Attribute(AttributeName.CHA, d((6, 6, 6), capl=2, caph=5)),
            accuracy=Attribute(AttributeName.ACC, d((6, 6, 6), capl=2, caph=5)),
        )

    @property
    def is_complete(self):
        return len(self._pending) == 0

