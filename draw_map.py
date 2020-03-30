import csv
import math
import numpy as np
from PIL import Image, ImageDraw


from simulation import Star


STARS = 'HabHyg_local.csv'
ROUTES = 'routes.csv'
MAP = 'map.png'

# Dimensions of map in parsecs
MAP_PC = (40,40)
# Map scale in pixels/parsec
MAP_SCALE = 40

ANGLE_X = math.radians(75)
ANGLE_Z = math.radians(10)
ROT_X = np.array([
    [1, 0, 0],
    [0, math.cos(ANGLE_X), -math.sin(ANGLE_X)],
    [0, math.sin(ANGLE_X), math.cos(ANGLE_X)],
])
ROT_Z = np.array([
    [math.cos(ANGLE_Z), -math.sin(ANGLE_Z), 0],
    [math.sin(ANGLE_Z), math.cos(ANGLE_Z), 0],
    [0, 0, 1],
])

# Size of our image as a function of map dimensions and scale
IMG_SIZE = (MAP_PC[0]*MAP_SCALE, MAP_PC[1]*MAP_SCALE)

def projection(x,y,z=None):
    # We'll skip the z rotation for 2D elements
    if z is None:
        z = 0
        z_rot = False
    else:
        z_rot = True

    # Ensure proper types for our input
    coords = np.array([
        float(x),
        float(y),
        # Not sure why, but we need to invert z here to get galactic north/south
        # to show up properly at the top/bottom of the image
        float(-z),
    ])

    if z_rot:
        # Rotation around z-axis
        coords = np.matmul(coords, ROT_Z)
        pass

    ## Rotation around x-axis
    coords = np.matmul(coords, ROT_X)

    ## DROP Z HERE
    ## This is where z stops mattering for our orthographic projection

    # Translate origin to upper left of image
    px = MAP_PC[0]/2 + coords[0]
    py = MAP_PC[1]/2 + coords[1]

    # Scale
    px = px * MAP_SCALE
    py = py * MAP_SCALE

    # Round
    px = round(px)
    py = round(py)

    return px, py

def draw_ui(img):
    ui = ImageDraw.Draw(img)

    for r in range(0,6):
        r = (r + 1) * 5
        r = r / 2

        ui.ellipse([projection(-r,-r),projection(r,r)], outline=(136,136,136,255), width=2)

    ui.line([projection(0,-17,0),projection(0,17,0)], fill=(136,136,136,255), width=2)
    ui.line([projection(-17,0,0),projection(17,0,0)], fill=(136,136,136,255), width=2)

    ui.ellipse([projection(-17,-17),projection(17,17)], outline=(238,238,238,255), width=2)

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

        pos = projection(*star.coords)
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

        routes.line([projection(*a.coords), projection(*b.coords)], color, width=1)

out = Image.alpha_composite(img, overlay)
out.save(MAP)

