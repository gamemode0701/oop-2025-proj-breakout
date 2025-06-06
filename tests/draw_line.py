"""
File: draw_line.py
Name:110613024 呂信吾
-------------------------
This file creates a window in which the user can repeatedly select two points and connect them with a straight line
until the window is closed
"""

from campy.graphics.gobjects import GOval, GLine
from campy.graphics.gwindow import GWindow
from campy.gui.events.mouse import onmouseclicked

window = GWindow()
num = 0
x0 = 0
y0 = 0


def main():
    """
    This program creates lines on an instance of GWindow class.
    There is a circle indicating the user’s first click. A line appears
    at the condition where the circle disappears as the user clicks
    on the canvas for the second time.
    """
    onmouseclicked(connect)


def connect(mouse):
    global num, x0, y0
    if num == 0:
        oval = GOval(10, 10)
        window.add(oval, x=mouse.x - 5, y=mouse.y-5)
        x0 = mouse.x
        y0 = mouse.y
        num += 1
    elif num == 1:
        maybe_obj = window.get_object_at(x0, y0)
        if maybe_obj is not GLine:
            window.remove(maybe_obj)
        line = GLine(x0, y0, mouse.x, mouse.y)
        window.add(line)
        num -= 1


if __name__ == "__main__":
    main()
