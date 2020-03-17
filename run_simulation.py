import csv
import random


from simulation import HyperspaceNetwork,Galaxy


STARS = 'HabHyg_local.csv'
PROB_PER_STEP = 0.40
STEPS = 120

galaxy = Galaxy.from_file(STARS)

network = HyperspaceNetwork(galaxy)

network2 = HyperspaceNetwork(galaxy, min_agents=2)

networks = [network,network2]

for i in range(STEPS):
    for n in networks:
        n.explore()

print('Found {routes} routes connecting {stars} stars'.format(
    routes=sum([len(list(n.routes)) for n in networks]),
    stars=sum([len(n.stars) for n in networks]),
))


with open('routes.csv', 'w', newline='') as csvfile:
    fieldnames = ['Owner','A','B','Distance','AB','BA']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for route in network.routes:
        writer.writerow({
            'Owner': 'Red',
            'A': route.a.name,
            'B': route.b.name,
            'Distance': route.dist,
            'AB': route.ab,
            'BA': route.ba,
        })

    for route in network2.routes:
        writer.writerow({
            'Owner': 'Green',
            'A': route.a.name,
            'B': route.b.name,
            'Distance': route.dist,
            'AB': route.ab,
            'BA': route.ba,
        })


