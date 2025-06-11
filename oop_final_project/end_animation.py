import random
from campy.graphics.gobjects import GRect, GLabel
from campy.gui.events.timer import pause
from campy.graphics.gwindow import GWindow
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
    # Calculate bounds
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)

    art_width = max_x - min_x
    art_height = max_y - min_y

    # Compute offsets to center the art in the window
    x_offset = (window.width - art_width) // 2 - min_x
    y_offset = (window.height - art_height) // 2 - min_y

    # Apply offsets
    coords = [(x + x_offset, y + y_offset) for x, y in coords]

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

def win_animation(window):
    text = GLabel("YOU WIN!")
    text.font = "-40-bold"
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "cyan", "magenta"]
    window.add(text, x=(window.width - text.width) / 2, y=window.height / 2)
    # Animate color changes
    for _ in range(30):  # about 3 seconds at 0.1s per frame
        text.color = random.choice(colors)
        pause(100)  # 0.1 seconds
    

    # Simple confetti effect
    for _ in range(150):
        x = random.randint(0, window.width)
        y = random.randint(0, window.height)
        dot = GLabel("*")
        dot.font = "-20"
        dot.color = random.choice(colors)
        window.add(dot, x=x, y=y)
        pause(10)

def game_over_menu(window):
    from campy.gui.events.mouse import onmouseclicked

    options = ['retry', 'back to menu', 'exit']
    choice = {'value': None}
    labels = []

    spacing = window.width // 4
    for i, text in enumerate(options):
        label = GLabel(text)
        label.font = '-20'
        label.color = 'crimson'
        x = (window.width - label.width) / 2
        y = window.height / 2 + i * spacing
        window.add(label, x, y)
        label.option = text
        labels.append(label)

    def click_handler(event):
        for label in labels:
            if label.x <= event.x <= label.x + label.width and label.y - 20 <= event.y <= label.y:
                choice['value'] = label.option

    onmouseclicked(click_handler)

    while choice['value'] is None:
        pause(100)

    for label in labels:
        window.remove(label)

    # 對應回傳英文標籤
    if choice['value'] == 'retry':
        return 'retry'
    elif choice['value'] == 'back to menu':
        return 'menu'
    else:
        return 'exit'
    
    
