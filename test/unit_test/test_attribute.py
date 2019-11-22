from src import attribute
from datetime import date


def test_handle_value_returns_default_if_value_is_none():
    test_attribute = attribute(default="hello")
    assert test_attribute.handle_value(None) == "hello"


def test_handle_value_return_decoded_value():
    test_attribute = attribute(decoder=date.fromisoformat)
    assert test_attribute.handle_value("2019-07-04") == date(2019, 7, 4)
