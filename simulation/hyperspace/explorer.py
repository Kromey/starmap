import math
import random


from simulation.hyperspace.route import HyperspaceRoute


class Explorer:
    def __init__(self, galaxy, discovery_odds=0.2, max_dist=5.3):
        self.__galaxy = galaxy
        self.__odds = discovery_odds

        self.max_dist = max_dist
        self.position = galaxy[0]

        self.__fail_count = 0

    def explore(self):
        if random.random() < self.__odds:
            self.__fail_count = 0
            print('Found one at', self.__odds, 'odds')
            self.__odds = 1 - (0.999 * (1 - self.__odds))
            print('\tOdds now', self.__odds)

            neighbors = self._get_neighbors()
            other = neighbors[math.floor(abs(random.random() - random.random()) * len(neighbors))]

            d = self.position.dist(other)

            ab = d * (1 + random.random() - random.random())
            ba = d * (1 + random.random() - random.random())

            print('Yay! Got one! From: {sn}; To: {en}; Distance: {d}; AB: {ab}; BA: {ba}'.format(
                sn=self.position.name,
                en=other.name,
                d=d,
                ab=ab,
                ba=ba,
            ))

            route = HyperspaceRoute(self.position, other, ab, ba)
            self.position = other

            return route
        else:
            self.__fail_count += 1
            print('I failed! Odds were', self.__odds, self.__fail_count, self.is_dead, self.is_alive)
            return None

    @property
    def is_dead(self):
        return self.__fail_count > 10

    @property
    def is_alive(self):
        return not self.is_dead

    def _get_neighbors(self):
        neighbors = []

        for other in self.__galaxy:
            d = self.position.dist(other)

            if d > 0 and d < self.max_dist:
                neighbors.append(other)

        neighbors.sort(key=lambda x: self.position.dist(x))

        return neighbors

