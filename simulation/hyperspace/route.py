class HyperspaceRoute:
    def __init__(self, a, b, ab, ba):
        self.__a = a
        self.__b = b
        self.__ab = ab
        self.__ba = ba

    def as_dict(self):
        return {
            'a': self.a.name,
            'b': self.b.name,
            'ab': self.ab,
            'ba': self.ba,
        }

    def update(self, other):
        if self.a == other.a and self.b == other.b:
            if other.ab < self.ab:
                self.__ab = other.ab
            if other.ba < self.ba:
                self.__ba = other.ba
        elif self.a == other.b and self.b == other.a:
            self.update(other.reverse())
        else:
            raise ValueError('Route Mismatch!')

    def reverse(self):
        return HyperspaceRoute(
            a=self.b,
            b=self.a,
            ab=self.ba,
            ba=self.ab,
        )

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def ab(self):
        return self.__ab

    @property
    def ba(self):
        return self.__ba

    @property
    def dist(self):
        return self.a.dist(self.b)

