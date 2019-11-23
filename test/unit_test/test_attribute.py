from src import attribute
from src.attribute import MISSING
from datetime import date


def test_handle_value_returns_default_if_value_is_none():
    test_attribute = attribute(default="hello")
    assert test_attribute.handle_value(MISSING, str) == "hello"


def test_handle_value_return_decoded_value():
    test_attribute = attribute(decoder=date.fromisoformat)
    assert test_attribute.handle_value("2019-07-04", date) == date(2019, 7, 4)


def test_handle_value_returns_plain_value_if():
    test_attribute = attribute()
    assert test_attribute.handle_value("huhu", str) == "huhu"
