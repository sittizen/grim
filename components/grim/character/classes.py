class Class:
    name: str
    # tweaks: list[TweakChoice]


class Fighter(Class):
    name = "fighter"
    # tweaks = [TweakChoice("pa", (Tweak(Save.PA, 1),)), TweakChoice("mfx", (Tweak(Save.MFX, -1),))]


class Cleric(Class):
    name = "cleric"
    # tweaks = [
    # TweakChoice("mfx", (Tweak(Save.MFX, 1),)),
    # ]


class Ranger(Fighter):
    name = "ranger"
