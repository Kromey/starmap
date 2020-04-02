import math
import random


from simulation.hyperspace.explorer import Explorer
from simulation.hyperspace.route import HyperspaceRoute


class HyperspaceNetwork:
    def __init__(self, owner, galaxy, max_dist=5.3, min_agents=1):
        self.__owner = owner
        self.__galaxy = galaxy
        self.__routes = []
        self.__explored = set()
        self.__explorers = []

        self.max_dist = max_dist
        self.min_agents = min_agents

        self.add_star(galaxy[0])

    def add_star(self, star):
        self.__explored.add(star)

    def explore(self):
        # Make sure we have our minimum number of explorers
        for x in range(self.min_agents - len(self.__explorers)):
            if random.random() < 0.25:
                self.spawn_explorer()

        if random.random() < 0.05:
            self.spawn_explorer()

        for exp in self.__explorers:
            route = exp.explore()

            if route is not None:
                self._add_route(route)

        self.__explorers = [exp for exp in self.__explorers if exp.is_alive]

    def spawn_explorer(self):
        exp = Explorer(self.__galaxy, max_dist = self.max_dist)

        stars = self.stars
        #stars.sort(key=self._get_cost)

        exp.position = stars[math.floor(abs(random.random() - random.random()) * len(stars))]

        self.__explorers.append(exp)

    @property
    def owner(self):
        return self.__owner

    @property
    def routes(self):
        for route in self.__routes:
            yield route

    @property
    def stars(self):
        return list(self.__explored)

    def _get_cost(self, dest, start=None, visited=None):
        if start is None:
            start = self.__galaxy[0]

        # Stop if we're there
        if dest == start:
            return 0

        # Find all routes from this star
        routes = []
        for route in self.__routes:
            if start in (route.a, route.b):
                routes.append(route)

        # Stop if we have no routes
        if len(routes) == 0:
            return None

        try:
            visited = visited[:]
        except TypeError:
            visited = []
        visited.append(start)

        cost = None

        for route in routes:
            if route.a == start:
                other = route.b
                other_cost = route.ab
            else:
                other = route.a
                other_cost = route.ba

            if other == dest:
                return other_cost
            elif other not in visited:
                if cost is None:
                    cost = other_cost
                elif other_cost > cost:
                    continue

                c = self._get_cost(dest, other, visited)
                if c is not None:
                    cost = min(cost, c)

        if cost:
            cost += self.stop_cost
            if len(routes) > 3:
                cost *= self.hub_factor

        return cost

    def _get_candidates(self, start):
        candidates = []

        for other in self.__galaxy:
            d = start.dist(other)

            if d > 0 and d < self.max_dist:
                candidates.append(other)

        candidates.sort(key=lambda x: start.dist(x))

        return candidates

    def _add_route(self, route):
        self.add_star(route.a)
        self.add_star(route.b)

        for r in self.__routes:
            try:
                r.update(route)
                return
            except ValueError:
                pass

        self.__routes.append(route)

