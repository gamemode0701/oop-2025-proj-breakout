from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLabel, GRect
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import sys


class WelcomeScreen:
    def __init__(self):
        self.window = GWindow(400, 600, title='Welcome to Breakout')
        self.level_selected = None
        self.buttons = []

        self.create_button('Default Layout', 100, 'default')
        self.create_button('Cross Layout', 200, 'cross')
        self.create_button('Zigzag Layout', 300, 'zigzag')
        self.create_button('Exit Game', 400, 'exit')

        onmouseclicked(self.handle_click)
        onmousemoved(self.handle_hover)

    def show(self):
        self.level_selected = None  # Reset selection each time shown

    def create_button(self, text, y_pos, layout_type):
        rect = GRect(300, 40)
        rect.layout_type = layout_type
        self.window.add(rect, x=50, y=y_pos)
        self.buttons.append(rect)
        rect.filled = True
        rect.fill_color = 'red' if layout_type == 'exit' else 'yellow'  # Exit 紅色，其餘黃色
        label = GLabel(text)
        label.font = 'Consolas-20'
        self.window.add(label, x=50 + (300 - label.width) / 2, y=y_pos + 35)

    def handle_click(self, event):
        for btn in self.buttons:
            if btn.x <= event.x <= btn.x + btn.width and btn.y <= event.y <= btn.y + btn.height:
                layout = btn.layout_type
                if layout == 'exit':
                    self.window.close()   # 先關閉 Campy 視窗
                    sys.exit()
                else:
                    self.level_selected = layout

    def handle_hover(self, event):
        for btn in self.buttons:
            if btn.x <= event.x <= btn.x + btn.width and btn.y <= event.y <= btn.y + btn.height:
                # 滑鼠在上面時，Exit 變深紅，其餘變淺藍
                btn.fill_color = '#b22222' if btn.layout_type == 'exit' else 'cyan'
            else:
                # 恢復原色
                btn.fill_color = 'red' if btn.layout_type == 'exit' else 'yellow'
