import csv
import json
import os
from PIL import Image, ImageDraw


from render import Projection, Star, UI
from simulation import CorpLoader,Galaxy


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

corps = CorpLoader.from_json('corps.json')
corps = {corp.short:corp for corp in corps}

with open('route_history.json','r') as fh:
    history = json.load(fh)

for time,routes in history:
    for route in routes:
        route['a'] = stars[route['a']]
        route['b'] = stars[route['b']]

        route['color'] = corps[route['owner']].color

os.makedirs('frames', exist_ok=True)
frame_counter = 0
total_frames = 720
rotation_factor = 360/total_frames
frames_per_step = 5

print('Exporting frames:')
for i in range(total_frames):
    pct = round(10 * (i/total_frames))
    print('\r[{bar}{empty}] {frames}/{total}'.format(
        bar='#'*pct,
        empty='.'*(10-pct),
        frames=frame_counter+1,
        total=total_frames,
    ), end='')

    projection.set_rotation(z=-i*rotation_factor)

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

    time = i // frames_per_step
    overlay_routes = ImageDraw.Draw(overlay)
    for t,routes in history:
        if t <= time:
            age = i - t * frames_per_step

            for route in routes:
                if t >= time-1:
                    overlay_routes.line(
                        projection.points([route['a'].coords, route['b'].coords]),
                        route['color'] + (64-age*6,),
                        width=5,
                    )

                overlay_routes.line(
                    projection.points([route['a'].coords, route['b'].coords]),
                    route['color'] + (255,),
                    width=1,
                )

    frame = Image.alpha_composite(img, overlay)
    frame.save('frames/frame-{:03}.png'.format(frame_counter))
    frame_counter += 1


print()
print('All frames exported!')

