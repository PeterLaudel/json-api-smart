from typing import Type, Union


def is_generic(type_: Type) -> bool:
    return hasattr(type_, "__origin__")


def is_union(some_type: Type) -> bool:
    if is_generic(some_type) and some_type.__origin__ == Union:
        return True

    return False


def is_optional(some_type: Type) -> bool:
    if is_union(some_type) is False:
        return False

    if type(None) in some_type.__args__:
        return True

    return False
