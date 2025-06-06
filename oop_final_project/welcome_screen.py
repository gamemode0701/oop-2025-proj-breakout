from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLabel, GRect
from campy.gui.events.mouse import onmouseclicked
import sys


class WelcomeScreen:
    def __init__(self):
        self.window = GWindow(400, 300, title='Welcome to Breakout')
        self.level_selected = None
        self.buttons = []

        self.create_button('Default Layout', 50, 'default')
        self.create_button('Cross Layout', 120, 'cross')
        self.create_button('Zigzag Layout', 190, 'zigzag')
        self.create_button('Exit Game', 260, 'exit')

        onmouseclicked(self.handle_click)

    def create_button(self, text, y_pos, layout_type):
        rect = GRect(300, 40)
        rect.filled = True
        rect.fill_color = 'yellow'
        rect.layout_type = layout_type  # MUST set before adding to window
        self.window.add(rect, x=50, y=y_pos)
        self.buttons.append(rect)

        label = GLabel(text)
        label.font = '-20'
        self.window.add(label, x=50 + (300 - label.width) / 2, y=y_pos + 28)

    def handle_click(self, event):
        for btn in self.buttons:
            if btn.x <= event.x <= btn.x + btn.width and btn.y <= event.y <= btn.y + btn.height:
                layout = btn.layout_type
                if layout == 'exit':
                    exit()
                else:
                    self.level_selected = layout
                    self.window._tkwin.withdraw()
