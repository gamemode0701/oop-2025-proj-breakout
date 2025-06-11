import random
from campy.graphics.gobjects import GLabel
from campy.gui.events.mouse import onmouseclicked
from campy.gui.events.timer import pause

def choose_from_two_powerups(window):
    """
    Display two randomly chosen power-up options on the window.
    Wait for the player to click one and return the selected power-up kind.
    """
    all_options = ['add_ball', 'multi_ball', 'slow', 'bomb', 'wide_paddle']
    options = random.sample(all_options, 2)
    labels = []
    selected = {'choice': None}

    # Layout options horizontally
    spacing = window.width // 3
    for i, opt in enumerate(options):
        label = GLabel(opt)
        label.font = '-20'
        label.color = 'darkgreen'
        x = spacing * (i + 1) - label.width / 2
        y = window.height / 2
        window.add(label, x, y)
        label.option = opt
        labels.append(label)

    # Define the click handler
    def handle_click(event):
        for label in labels:
            if (label.x <= event.x <= label.x + label.width) and (label.y - 20 <= event.y <= label.y):
                selected['choice'] = label.option

    # Register mouse event
    onmouseclicked(handle_click)

    # Wait until selection is made
    while selected['choice'] is None:
        pause(100)

    # Clean up labels
    for label in labels:
        window.remove(label)

    return selected['choice']
