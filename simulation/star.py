from collections import namedtuple
from collections.abc import MutableSequence
import csv
import math


class Galaxy(MutableSequence):
    def __init__(self):
        self.__stars = []

    def add_star(self, star, min_dist=0.11):
        for i in range(len(self)):
            neighbor = self[i]
            if star.dist(neighbor) < min_dist:
                if star.absmag < neighbor.absmag:
                    self[i] = star
                return

        self.append(star)

    @classmethod
    def from_file(cls, filename):
        g = cls()

        with open(filename, 'r', newline='') as fh:
            reader = csv.DictReader(fh)
            for star in reader:
                g.add_star(Star.from_dict(star))

        return g

    def known_to(self, corp):
        try:
            corp = corp.short
        except AttributeError:
            # Assume we were given a short name instead of an object
            pass

        for star in self:
            if star.name == 'Sol':
                yield star
                continue

            for route in star.routes:
                if route.owner.short == corp:
                    yield star
                    break

    def __getitem__(self, i):
        return self.__stars[i]

    def __setitem__(self, i, value):
        self.__stars[i] = value

    def __delitem__(self, i):
        del self.__stars[i]

    def insert(self, i, value):
        return self.__stars.insert(i, value)

    def __len__(self):
        return len(self.__stars)


class Route:
    def __init__(self, owner, to, time):
        self.owner = owner
        self.to = to
        self.time = time

    def update(self, owner, to, time):
        if self.owner != owner or self.to != to:
            raise ValueError('Route Mismatch!')

        self.time = min(self.time, time)

class Star:
    def __init__(self, name, is_habitable, spectral_class, absmag, coords):
        self.__name = name
        self.__is_habitable = is_habitable
        self.__spectral_class = spectral_class
        self.__absmag = absmag
        self.__coords = coords

        self.__routes = []

    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data['Display Name'],
            is_habitable = data['Hab?'].strip() == '1',
            spectral_class = data['Spectral Class'],
            absmag = float(data['AbsMag']),
            coords = (
                float(data['Xg']),
                float(data['Yg']),
                float(data['Zg']),
            ),
        )

    def dist(self, other=None):
        if other:
            coords = other.coords
        else:
            coords = (0,0,0) # Distance from Sol

        s = 0
        for a,b in zip(self.coords, coords):
            s += (a - b)**2

        return math.sqrt(s)

    def add_route(self, corp, to, time):
        for route in self.routes:
            try:
                route.update(corp, to, time)
                print('\tUpdated route!')
                return
            except ValueError:
                pass

        self.__routes.append(Route(corp, to, time))

    @property
    def name(self):
        return self.__name

    @property
    def is_habitable(self):
        return self.__is_habitable

    @property
    def spectral_class(self):
        return self.__spectral_class

    @property
    def absmag(self):
        return self.__absmag

    @property
    def coords(self):
        return self.__coords

    @property
    def routes(self):
        for route in self.__routes:
            yield route

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Star<{}>'.format(str(self))

    def __hash__(self):
        return hash((self.name, self.coords))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

