from collections.abc import Iterable
from enum import Enum
from typing import Any


class Tweak:
    """A tweak can be applied to rolled value of Stats when building a character."""

    def __init__(self, stat: Enum, tweak: int):
        self.cat: type[Enum] = type(stat)
        self.stat: Enum = stat
        self.tweak: int = tweak


class Stats:
    """Defines a logical group of stats, each with an integer value."""

    def __init__(self, enum: type[Enum]):
        self._enum = enum
        self._layers: set[str] = set()
        self._tweaks: dict[
            str,
            dict[
                str,
                int,
            ],
        ] = {}
        for member in self._enum:
            setattr(self, member.name, 0)

    def __getattribute__(self, name: str) -> Any:
        if name in ("_enum", "_layers", "_tweaks", "tweak", "apply", "remove", "layers"):
            return super().__getattribute__(name)
        if name in self._enum.__members__:
            out = super().__getattribute__(name)
            for layer in self._layers:
                if layer in self._tweaks and name in self._tweaks[layer]:
                    out += self._tweaks[layer][name]
            return out

    def __iter__(self) -> Iterable[Enum]:
        return iter(self._enum)

    @property
    def layers(self) -> set[str]:
        return self._layers

    def tweak(self, name: str, stat: Enum, val: int) -> None:
        if name not in self._tweaks:
            self._tweaks[name] = {stat.name: val}
        elif name in self._tweaks and stat.name not in self._tweaks[name]:
            self._tweaks[name][stat.name] = val
        else:
            raise ValueError(f"Tweak {name} already exists for {stat}")

    def apply(self, layer: str) -> None:
        if layer in self._layers:
            raise ValueError(f"Layer {layer} already applied")
        self._layers.add(layer)

    def remove(self, layer: str) -> None:
        if layer not in self._layers:
            raise ValueError(f"Layer {layer} not applied")
        self._layers.remove(layer)
