from typing import TypeVar, Union, Dict, Type

T = TypeVar("T")


class Attribute:
    def __init__(self, decoder):
        self.decoder = decoder


def attribute(decoder=None):
    return Attribute(decoder=decoder)
