from random import randrange

def d(faces: int, adv: int = 0, dis: int = 0) -> int:
    take =  max if adv - dis >= 0 else min
    rolls = abs(adv - dis) + 1
    return take([randrange(1, faces + 1) for _ in range(rolls)], key=lambda x: x)
