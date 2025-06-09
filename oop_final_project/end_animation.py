import random
from campy.graphics.gobjects import GRect
from campy.gui.events.timer import pause
import os

def lost_animation(window):
    window.clear()
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'location.txt')
    coords = []
    x = None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # skip empty lines
                continue
            if line.startswith('x') and line[1:].isdigit():
                x = int(line[1:])
            elif line.startswith('y') and line[1:].isdigit() and x is not None:
                y = int(line[1:])
                coords.append((x, y))
                x = None  # reset x
            # Skip label lines like 'G1', 'A2', etc.

    print(f"Total coords parsed: {len(coords)}")  # DEBUG

    for x, y in coords:
        pixel = GRect(6, 6)
        pixel.filled = True
        pixel.fill_color = 'crimson'
        pixel.color = 'crimson'
        window.add(pixel, x=x, y=y)
        pause(1)

    pause(3000)

    # Fade-out
    fade_count = 0
    total_to_fade = len(coords)
    while fade_count < total_to_fade:
        i = random.randint(0, len(coords) - 1)
        x, y = coords[i]
        obj = window.get_object_at(x + 3, y + 3)
        if obj is not None:
            window.remove(obj)
            fade_count += 1
            pause(2)

