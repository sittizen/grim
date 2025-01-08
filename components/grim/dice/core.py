from random import randrange


def d(
    *args: int,
    adv: int = 0,
    dis: int = 0,
    capl: int = 1,
    caph: int | None = None,
) -> int:
    """
    Simulates rolling dice with optional advantage, disadvantage, and capping.

    Parameters:
        *args (int): One or more integers representing the number of faces on each die.
        adv (int, optional): Number of advantage rolls. Defaults to 0.
        dis (int, optional): Number of disadvantage rolls. Defaults to 0.
        capl (int, optional): Minimum cap for the roll result. Defaults to 1.
        caph (int | None, optional): Maximum cap for the roll result. Defaults to None.

    Returns:
        int: The resulting sum of dice rolls, after applying advantage/disadvantage and capping.
    """
    if len(args) == 1:
        faces = args[0]
        caph = caph or faces
        take = max if adv - dis >= 0 else min
        rolls = abs(adv - dis) + 1
        out = take([randrange(1, faces + 1) for _ in range(rolls)], key=lambda x: x)
        return min(max(out, capl), caph)
    out = 0
    for f in args:
        out += d(f, adv=adv, dis=dis, capl=capl, caph=caph)
    return out
