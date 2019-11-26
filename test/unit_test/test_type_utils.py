from typing import List, Union, Optional
from src.type_utils import is_generic, is_union, is_optional, is_list


def test_is_generic():
    assert is_generic(List) is True


def test_is_generic_returns_false():
    class SomeNotGeneric:
        pass

    assert is_generic(SomeNotGeneric) is False


def test_is_union():
    assert is_union(Union[int, str]) is True


def test_is_union_is_false():
    assert is_union(List[int]) is False


def test_is_optional():
    assert is_optional(Optional[int]) is True


def test_is_optional_returns_false():
    assert is_optional(Union[str, int]) is False


def test_is_list():
    assert is_list(List[str]) is True


def test_is_list_returns_false():
    assert is_list(Union[str]) is False
