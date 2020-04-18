import math
import random


from simulation.hyperspace.route import HyperspaceRoute


class Explorer:
    def __init__(self, corp, discovery_odds=0.2, max_dist=5.3):
        self.corp = corp
        self.max_dist = max_dist
        self.position = corp.galaxy[0]

        self.__odds = discovery_odds
        self.__discoveries = 0

    def explore(self):
        if random.random() < self.__odds:
            self.__discoveries += 1

            neighbors = self._get_neighbors()
            other = neighbors[math.floor(abs(random.random() - random.random()) * len(neighbors))]

            d = self.position.dist(other)

            ab = d * (1 + random.random() - random.random())
            ba = d * (1 + random.random() - random.random())

            print('{corp}: From: {sn}; To: {en}; Distance: {d}; AB: {ab}; BA: {ba}'.format(
                corp=self.corp,
                sn=self.position.name,
                en=other.name,
                d=d,
                ab=ab,
                ba=ba,
            ))

            self.position.add_route(self.corp, other, ab)
            other.add_route(self.corp, self.position, ba)

            route = {
                'corp': self.corp.short,
                'from': self.position.name,
                'to': other.name,
                'time_to': ab,
                'time_from': ba,
            }

            self.position = other

            return route
        else:
            return None

    @property
    def is_dead(self):
        return random.random() < 0.25 * (self.__discoveries - 2)

    @property
    def is_alive(self):
        return not self.is_dead

    def _get_neighbors(self):
        neighbors = []

        for other in self.corp.galaxy:
            d = self.position.dist(other)

            if d > 0 and d < self.max_dist:
                neighbors.append(other)

        neighbors.sort(key=lambda x: self.position.dist(x))

        return neighbors

