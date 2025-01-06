from grim.stats import Tweak, TweakChoice

from .stats import Attribute, Save


class Class:
    name: str
    main_attr: list[Attribute]
    tweaks: list[TweakChoice]


class Fighter(Class):
    name = "fighter"
    main_attr = [
        Attribute.STR,
        Attribute.DEX,
    ]
    tweaks = [TweakChoice("pa", (Tweak(Save.PA, 1),)), TweakChoice("mfx", (Tweak(Save.MFX, -1),))]


class Cleric(Class):
    name = "cleric"
    main_attr = [Attribute.PER, Attribute.CHA]
    tweaks = [
        TweakChoice("mfx", (Tweak(Save.MFX, 1),)),
    ]


class Ranger(Fighter):
    name = "ranger"
    main_attr = [Attribute.DEX]
