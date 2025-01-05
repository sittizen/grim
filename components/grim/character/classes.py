from .stats import Attribute


class Class:
    name: str
    main_attr: list[Attribute]


class Fighter(Class):
    name = "fighter"
    main_attr = [
        Attribute.STR,
    ]
