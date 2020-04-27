import csv
import json
import random


from simulation import Galaxy,CorpLoader


STARS = 'data/HabHyg_local.csv'
STEPS = 120

galaxy = Galaxy.from_file(STARS)

corps = CorpLoader.from_json('data/corps.json', galaxy)

history = []
for i in range(STEPS):
    routes = []
    for corp in corps:
        for route in corp.explore():
            routes.append(route)

    if routes:
        history.append([i, routes])

with open('data/route_history.json', 'w') as fh:
    json.dump(history, fh, indent=2)

print('Found {routes} routes connecting {stars} (or {stars2}) stars'.format(
    routes=sum([len(list(star.routes)) for star in galaxy]),
    stars=sum([len(list(corp.stars)) for corp in corps]),
    stars2=len([star for star in galaxy if list(star.routes)]),
))


