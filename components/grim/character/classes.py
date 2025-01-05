from grim.stats import Tweak

from .stats import Attribute, Save


class Class:
    name: str
    main_attr: list[Attribute]
    tweaks: dict[str, tuple[list[Tweak], ...]]


class Fighter(Class):
    name = "fighter"
    main_attr = [
        Attribute.STR,
        Attribute.DEX,
    ]
    tweaks = {"saves": ([Tweak(cat=Save, stat=Save.PA, val=1)], [Tweak(cat=Save, stat=Save.MFX, val=-1)])}


class Ranger(Fighter):
    name = "ranger"
    main_attr = [Attribute.DEX]
