from typing import TypeVar, Union, Dict, Type

T = TypeVar("T")


class MISSING:
    pass


class Attribute:
    def __init__(self, decoder, encoder, default):
        self.decoder = decoder
        self.encoder = encoder
        self.default = default

    def handle_value(self, value: Union[str, int, Dict], value_type: Type[T]) -> T:
        if value is MISSING and self.default is not MISSING:
            return self.default

        if self.decoder is not None:
            return self.decoder(value)

        return value_type(value)


def attribute(decoder=None, encoder=None, default=MISSING):
    return Attribute(decoder=decoder, encoder=encoder, default=default)
