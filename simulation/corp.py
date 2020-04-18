import json
import math
import random


from simulation.explorer import Explorer


class CorpLoader:
    @staticmethod
    def from_json(fname, galaxy):
        with open(fname, 'r') as fh:
            data = json.load(fh)

        return [Corp(galaxy=galaxy, **corp) for corp in data]


class Corp:
    def __init__(self, name, color, galaxy, short_name=None, explorers=None):
        self.name = name
        self.color = tuple(color)

        self.short = short_name or Corp.shorten(name)

        self.galaxy = galaxy

        if explorers is None:
            self.explorer_params = {}
        else:
            self.explorer_params = explorers

        try:
            self.min_explorers = self.explorer_params['minimum_explorers']
            del self.explorer_params['minimum_explorer']
        except KeyError:
            self.min_explorers = 3

        self.__explorers = []

    @staticmethod
    def shorten(name):
        return ''.join(c for c in name if c.isupper())

    @property
    def stars(self):
        return self.galaxy.known_to(self)

    def explore(self):
        # Spawn explorers
        self.spawn_explorers()

        for exp in self.__explorers:
            route = exp.explore()

            if route is not None:
                yield route

        self.__explorers = [exp for exp in self.__explorers if exp.is_alive]

    def spawn_explorers(self):
        stars = sorted(self.stars, key=lambda star: star.dist())

        for x in range(self.min_explorers - len(self.__explorers)):
            if random.random() < 0.50:
                self._new_explorer(stars)

        if random.random() < 0.05:
            self._new_explorer(stars)

    def _new_explorer(self, stars):
        exp = Explorer(self, **self.explorer_params)

        exp.position = stars[math.floor(abs(random.random() - random.random()) * len(stars))]

        self.__explorers.append(exp)

    def __str__(self):
        return self.short

