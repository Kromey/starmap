import json


class CorpLoader:
    @staticmethod
    def from_json(fname):
        with open(fname, 'r') as fh:
            data = json.load(fh)

        return [Corp(**corp) for corp in data]


class Corp:
    def __init__(self, name, color, short_name=None):
        self.name = name
        self.color = color

        self.short = short_name or Corp.shorten(name)

    @staticmethod
    def shorten(name):
        return ''.join(c for c in name if c.isupper())

