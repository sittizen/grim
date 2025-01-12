from enum import Enum

TweaksChoice = list[tuple[Enum, int]]


class Layer:
    name: str
    tweaks_choices: dict[str, TweaksChoice] = {}

    def __init__(self) -> None:
        self.layer: dict[str, dict[Enum, int]] = {}
        for tweak, choices in self.tweaks_choices.items():
            if len(choices) == 1:
                stat, val = choices[0][0], choices[0][1]
                self.layer[tweak] = {stat: val}

    @property
    def has_pending_choices(self) -> bool:
        return len(self.layer) != len(self.tweaks_choices)

    @property
    def pending_choices(self) -> dict[str, TweaksChoice]:
        return {k: v for k, v in self.tweaks_choices.items() if k not in self.layer}

    def choose(self, tweak: str, choice: Enum) -> None:
        choice_val = [c for c in self.tweaks_choices[tweak] if c[0] == choice][0][1]
        self.layer[tweak] = {choice: choice_val}
