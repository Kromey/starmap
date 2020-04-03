import csv
import json
import random


from simulation import HyperspaceNetwork,Galaxy,CorpLoader


STARS = 'HabHyg_local.csv'
STEPS = 120

galaxy = Galaxy.from_file(STARS)

corps = CorpLoader.from_json('corps.json')

networks = []
for corp in corps:
    networks.append(HyperspaceNetwork(corp, galaxy))

history = []
for i in range(STEPS):
    routes = []
    for n in networks:
        new = n.explore()
        if new:
            for r in new:
                r = r.as_dict()
                r['owner'] = n.owner.short
                routes.append(r)

    if routes:
        history.append([i, routes])

with open('route_history.json', 'w') as fh:
    json.dump(history, fh)

print('Found {routes} routes connecting {stars} stars'.format(
    routes=sum([len(list(n.routes)) for n in networks]),
    stars=sum([len(n.stars) for n in networks]),
))


with open('routes.csv', 'w', newline='') as csvfile:
    fieldnames = ['Owner','A','B','Distance','AB','BA']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for network in networks:
        for route in network.routes:
            writer.writerow({
                'Owner': network.owner.short,
                'A': route.a.name,
                'B': route.b.name,
                'Distance': route.dist,
                'AB': route.ab,
                'BA': route.ba,
            })


