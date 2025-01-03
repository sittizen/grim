from random import randrange


def d(
    faces: int | tuple[int, ...],
    adv: int = 0,
    dis: int = 0,
    capl: int = 1,
    caph: int | None = None,
) -> int:
    if isinstance(faces, int):
        caph = caph or faces
        take = max if adv - dis >= 0 else min
        rolls = abs(adv - dis) + 1
        out = take([randrange(1, faces + 1) for _ in range(rolls)], key=lambda x: x)
        return min(max(out, capl), caph)
    out = 0
    for f in faces:
        out += d(faces=f, adv=adv, dis=dis, capl=capl, caph=caph)
    return out
