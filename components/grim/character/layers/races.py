from enum import Enum

from ..stats import Attributes, Saves
from . import Layer

TweaksChoice = list[tuple[Enum, int]]


class Race(Layer):
    pass


class Human(Race):
    name = "human"


class Elf(Race):
    name = "elf"
    tweaks_choices: dict[str, TweaksChoice] = {
        "main_attribute": [(Attributes.DEX, 1), (Attributes.KNO, 1)],
        "save_mfx": [(Saves.MFX, 1)],
    }
