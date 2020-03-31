import csv
import math
import numpy as np
from PIL import Image, ImageDraw


from render import Projection
from simulation import Star


STARS = 'HabHyg_local.csv'
ROUTES = 'routes.csv'
MAP = 'map.png'

# Dimensions of map in parsecs
MAP_PC = (36,36)
# Map scale in pixels/parsec
MAP_SCALE = 40

projection = Projection(MAP_PC, MAP_SCALE, 75, 80)

# Size of our image as a function of map dimensions and scale
IMG_SIZE = (MAP_PC[0]*MAP_SCALE, MAP_PC[1]*MAP_SCALE)

def draw_ui(img):
    ui = ImageDraw.Draw(img)

    for r in range(0,6):
        r = (r + 1) * 2.5

        ui.ellipse(projection.ellipse((-r,-r),(r,r)), outline=(136,136,136,255), width=2)

    ui.line([projection.point(0,-17),projection.point(0,17)], fill=(136,136,136,255), width=2)
    ui.line([projection.point(-17,0),projection.point(17,0)], fill=(136,136,136,255), width=2)

    # Outermost ring is slightly different, so ensure it's above our lines
    ui.ellipse(projection.ellipse((-17,-17),(17,17)), outline=(238,238,238,255), width=2)

    ## Directional indicators
    ## Drawn last so they overlay our rings/lines
    # Coreward
    points = projection.points([
        (18,0),
        (16.6,0.45),
        (16.9,0),
        (16.6,-0.45),
    ])
    ui.polygon(points, fill=(0,0,255,255))

    # Spinward
    points = projection.points([
        (0,18),
        (0.45,16.6),
        (0,16.9),
        (-0.45,16.6),
    ])
    ui.polygon(points, fill=(255,0,0,255))

stars = {}
queue = {
    'lines': {
        'posz': [],
        'negz': [],
    },
    'stars': {
        'posz': [],
        'negz': [],
    },
}
with open(STARS, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for star in reader:
        star = Star.from_dict(star)
        stars[star.name] = star

        pos = projection.point(*star.coords)
        bounds = [
            (pos[0]-5, pos[1]-5),
            (pos[0]+5, pos[1]+5),
        ]

        if star.name == 'Sol':
            outline = (0,255,0,255)
        elif star.name == 'Gl 447':
            outline = (0,136,255,255)
        elif star.name == 'Gl 46':
            outline = (255,0,0,255)
        elif star.name == 'NN 4013':
            outline = (255,0,255,255)
        elif star.name == 'NN 4219':
            outline = (255,255,0,255)
        else:
            outline = (170,170,170,255)

        if star.is_habitable:
            fill = outline
        else:
            fill = (0,0,0,255)

        k = 'posz' if float(star.coords[2]) >= 0 else 'negz'
        queue['stars'][k].append((bounds, fill, outline))


img = Image.new('RGBA', IMG_SIZE, (0,0,0,255))

starmap = ImageDraw.Draw(img)

# Draw neg-z stars:
for star in queue['stars']['negz']:
    starmap.ellipse(star[0], fill=star[1], outline=star[2], width=2)

# Now draw UI "on top of" neg-z stars
draw_ui(img)

# Draw pos-z stars:
for star in queue['stars']['posz']:
    starmap.ellipse(star[0], fill=star[1], outline=star[2], width=2)


overlay = Image.new('RGBA', img.size, (255,255,255,0))
routes = ImageDraw.Draw(overlay)

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

