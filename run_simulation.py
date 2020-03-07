import csv


from simulation import HyperspaceNetwork,Galaxy


STARS = 'HabHyg_local.csv'

galaxy = Galaxy.from_file(STARS)

network = HyperspaceNetwork(galaxy, falloff=4)
network.add_star(galaxy[0])
for i in range(75):
    network.discover_route()

network2 = HyperspaceNetwork(galaxy, falloff=6)
network2.add_star(galaxy[0])
for i in range(60):
    network2.discover_route()


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


