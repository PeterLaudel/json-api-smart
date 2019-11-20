class MISSING:
    pass


class Attribute:
    def __init__(self, decoder, encoder, default):
        self.decoder = decoder
        self.encoder = encoder
        self.default = default

    def handle_value(self, value):
        if value is None and self.default is not MISSING:
            return self.default

        if self.decoder is not None:
            return self.decoder(value)

        return value


def attribute(decoder=None, encoder=None, default=MISSING):
    return Attribute(decoder=decoder, encoder=encoder, default=default)
