import csv
import json
import os
from PIL import Image, ImageDraw


from render import Projection, Star, UI
from simulation import CorpLoader,Galaxy


STARS = 'data/HabHyg_local.csv'
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

corps = CorpLoader.from_json('data/corps.json', galaxy)
corps = {corp.short:corp for corp in corps}

with open('data/route_history.json','r') as fh:
    history = json.load(fh)

for time,routes in history:
    for route in routes:
        route['a'] = stars[route['a']]
        route['b'] = stars[route['b']]

        route['color'] = corps[route['owner']].color

os.makedirs('frames', exist_ok=True)

frames_per_degree = 3
steps = 120
step_padding = 2

total_steps = steps + step_padding*2
total_frames = frames_per_degree * 360
frames_per_step = total_frames // total_steps

print('Exporting frames:')
for i in range(total_frames):
    pct = round(10 * (i/total_frames))
    print('\r[{bar}{empty}] {frames}/{total}'.format(
        bar='#'*pct,
        empty='.'*(10-pct),
        frames=i+1,
        total=total_frames,
    ), end='')

    projection.set_rotation(z=-i/frames_per_degree)

    img = Image.new('RGBA', IMG_SIZE, (0,0,0,255))

    stars_south = Image.new('RGBA', img.size, (0,0,0,0))
    stars_north = Image.new('RGBA', img.size, (0,0,0,0))

    south = ImageDraw.Draw(stars_south)
    north = ImageDraw.Draw(stars_north)

    # Draw stars:
    for star in galaxy:
        if star.coords[2] >= 0:
            starmap = north
        else:
            starmap = south

        starmap.ellipse(plotter.ellipse(star), fill=plotter.fill_color(star), outline=plotter.color(star), width=1)

    # Draw UI
    ui_overlay = Image.new('RGBA', img.size, (0,0,0,0))
    ui.draw(ui_overlay)

    # Blend stars and UI
    img = Image.alpha_composite(img, stars_south)
    img = Image.alpha_composite(img, ui_overlay)
    img = Image.alpha_composite(img, stars_north)

    overlay = Image.new('RGBA', img.size, (255,255,255,0))
    flares = Image.new('RGBA', img.size, (255,255,255,0))

    time = i // frames_per_step
    overlay_routes = ImageDraw.Draw(overlay)
    flare_draw = ImageDraw.Draw(flares)
    for t,routes in history:
        if t <= time:
            age = i - t * frames_per_step

            flare_alpha = 256 - (128+64)*(age/10)

            for route in routes:
                if t >= time-1:
                    for flare_size in range(5,0,-1):
                        flare_draw.line(
                            projection.points([route['a'].coords, route['b'].coords]),
                            route['color'] + (round(flare_alpha / (2 ** flare_size)),),
                            width=flare_size*2 + 1,
                        )

                overlay_routes.line(
                    projection.points([route['a'].coords, route['b'].coords]),
                    route['color'] + (255,),
                    width=1,
                )

    img = Image.alpha_composite(img, flares)
    img = Image.alpha_composite(img, overlay)
    img.save('frames/frame-{:03}.png'.format(i))


print()
print('All frames exported!')

