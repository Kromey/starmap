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
stars = {star.name:star for star in galaxy}

routes = []
with open(ROUTES, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for route in reader:
        route['A'] = stars[route['A']]
        route['B'] = stars[route['B']]

        if route['Owner'] == 'Red':
            color = (255,136,136,136)
        elif route['Owner'] == 'Green':
            color = (136,255,136,136)

        route['color'] = color

        routes.append(route)

frames = []

for i in range(0, 360, 3):
    projection.set_rotation(z=-i)

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

    overlay_routes = ImageDraw.Draw(overlay)
    for route in routes:
        overlay_routes.line(projection.points([route['A'].coords, route['B'].coords]), route['color'], width=1)

    frame = Image.alpha_composite(img, overlay)
    frames.append(frame)

frames[0].save('starmap.gif', save_all=True, append_images=frames[1:], optimize=True, duration=100, loop=0)


