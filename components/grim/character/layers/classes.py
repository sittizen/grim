from enum import Enum

from ..stats import Attributes, Saves
from . import Layer

TweaksChoice = list[tuple[Enum, int]]


class Class(Layer):
    pass


class Fighter(Class):
    name: str = "fighter"
    tweaks_choices: dict[str, TweaksChoice] = {
        "main_attribute": [(Attributes.STR, 1), (Attributes.DEX, 1)],
        "save_pa": [(Saves.PA, 1)],
        "save_mfx": [(Saves.MFX, -1)],
    }


class Cleric(Class):
    name = "cleric"
    # tweaks = [
    # TweakChoice("mfx", (Tweak(Save.MFX, 1),)),
    # ]


class Ranger(Fighter):
    name = "ranger"
