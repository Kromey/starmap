import csv
from PIL import Image, ImageDraw


from render import Projection, Star, UI
from simulation import Galaxy


STARS = 'HabHyg_local.csv'
ROUTES = 'routes.csv'
MAP = 'map.png'

# Dimensions of map in parsecs
MAP_PC = (36,36)
# Map scale in pixels/parsec
MAP_SCALE = 20

projection = Projection(MAP_PC, MAP_SCALE, 75, -5)
ui = UI(projection)
plotter = Star(projection)

# Size of our image as a function of map dimensions and scale
IMG_SIZE = (MAP_PC[0]*MAP_SCALE, MAP_PC[1]*MAP_SCALE)

galaxy = Galaxy.from_file(STARS)

img = Image.new('RGBA', IMG_SIZE, (0,0,0,255))

starmap = ImageDraw.Draw(img)

# Draw neg-z stars:
for star in galaxy:
    if star.coords[2] >= 0:
        continue

    starmap.ellipse(plotter.ellipse(star), fill=plotter.fill_color(star), outline=plotter.color(star), width=1)

# Now draw UI "on top of" neg-z stars
ui.draw(img)

# Draw pos-z stars:
for star in galaxy:
    if star.coords[2] < 0:
        continue

    starmap.ellipse(plotter.ellipse(star), fill=plotter.fill_color(star), outline=plotter.color(star), width=1)


overlay = Image.new('RGBA', img.size, (255,255,255,0))
routes = ImageDraw.Draw(overlay)

stars = {star.name:star for star in galaxy}

with open(ROUTES, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for route in reader:
        a = stars[route['A']]
        b = stars[route['B']]

        if route['Owner'] == 'Red':
            color = (255,136,136,136)
        elif route['Owner'] == 'Green':
            color = (136,255,136,136)

        routes.line([projection.point(*a.coords), projection.point(*b.coords)], color, width=1)

out = Image.alpha_composite(img, overlay)
out.save(MAP)

