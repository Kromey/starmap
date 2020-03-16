import csv
import random


from simulation import HyperspaceNetwork,Galaxy


STARS = 'HabHyg_local.csv'
PROB_PER_STEP = 0.40
STEPS = 200

galaxy = Galaxy.from_file(STARS)

network = HyperspaceNetwork(galaxy, falloff=4)
network.add_star(galaxy[0])
network.spawn_explorer()
network.spawn_explorer()

network2 = HyperspaceNetwork(galaxy, falloff=6)
network2.add_star(galaxy[0])
network2.spawn_explorer()

networks = [network,network2]

for i in range(STEPS):
    for n in networks:
        n.explore()


with open('routes.csv', 'w', newline='') as csvfile:
    fieldnames = ['Owner','A','B']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for route in network.routes:
        writer.writerow({
            'Owner': 'Red',
            'A': route.a.name,
            'B': route.b.name,
        })

    for route in network2.routes:
        writer.writerow({
            'Owner': 'Green',
            'A': route.a.name,
            'B': route.b.name,
        })


