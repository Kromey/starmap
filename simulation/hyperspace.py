import math
import random


class HyperspaceNetwork:
    def __init__(self, galaxy, max_dist=7.3, falloff=4.0, stop_cost=0.5, hub_factor=0.5):
        self.__galaxy = galaxy
        self.__routes = []
        self.__explored = []

        for s in galaxy:
            self.__routes.append(None)
            self.__explored.append(False)

        self.max_dist = max_dist
        self.falloff = falloff
        self.stop_cost = stop_cost
        self.hub_factor = hub_factor

    def add_star(self, star):
        self.__explored[self.__galaxy.index(star)] = True

    def discover_route(self):
        explored = self._get_explored()
        starti = explored[math.floor(random.random() ** (self.falloff/2) * len(explored))]
        start = self.__galaxy[starti]

        candidates = self._get_candidates(start)

        otheri = candidates[math.floor(random.random() ** self.falloff * len(candidates))]
        other = self.__galaxy[otheri]

        d = start.dist(other)

        ab = d * (random.random()*0.5 + 0.75)
        ba = d * (random.random()*0.5 + 0.75)

        print('Yay! Got one! From: ({si}) {sn}; To: ({ei}) {en}'.format(
            si=starti,
            sn=start.name,
            ei=otheri,
            en=other.name,
        ))

        self._add_route(starti, otheri, ab, ba)

    @property
    def routes(self):
        for a in range(len(self.__routes)):
            if self.__routes[a] is None:
                continue

            for b in self.__routes[a]:
                b = b[0]
                if b < a:
                    continue

                yield HyperspaceRoute(self.__galaxy[a], self.__galaxy[b])

    def _get_explored(self):
        explored = []

        for i in range(len(self.__explored)):
            if self.__explored[i]:
                cost = self._get_cost(i)

                explored.append((i,cost))

        explored.sort(key=lambda x: x[1])

        return [x[0] for x in explored]

    def _get_cost(self, dest, start=0, visited=None):
        # Stop if we're there
        if dest == start:
            return 0

        # Stop if we have no routes
        if self.__routes[start] is None:
            return None

        if visited is None:
            visited = [start]
        else:
            visited = visited[:]
            visited.append(start)

        cost = None

        for nxt in self.__routes[start]:
            if nxt[0] == dest:
                return nxt[1]
            elif nxt[0] not in visited:
                if cost is None:
                    cost = nxt[1]
                elif nxt[1] > cost:
                    continue

                c = self._get_cost(dest, nxt[0], visited)
                if c is not None:
                    cost = min(cost, c)

        if cost:
            cost += self.stop_cost
            if len(self.__routes[start]) > 3:
                cost *= self.hub_factor

        return cost

    def _get_candidates(self, start):
        candidates = []

        for i in range(len(self.__galaxy)):
            star = self.__galaxy[i]
            d = start.dist(star)

            if d > 0 and d < self.max_dist:
                candidates.append((i,d))

        candidates.sort(key=lambda x: x[1])

        return [candidate[0] for candidate in candidates]

    def _add_route(self, a, b, ab, ba, bi_d=True):
        self.add_star(self.__galaxy[a])

        if bi_d:
            self._add_route(b, a, ba, ab, False)

        route = (b, ab)
        if self.__routes[a] is None:
            self.__routes[a] = [route]
        else:
            for r in range(len(self.__routes[a])):
                if self.__routes[a][r][0] == b:
                    if ab < self.__routes[a][r][1]:
                        self.__routes[a][r] = route
                    return
            self.__routes[a].append(route)

class HyperspaceRoute:
    def __init__(self, a, b):
        self.__a = a
        self.__b = b

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

