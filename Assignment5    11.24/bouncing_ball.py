"""
File: bouncing_ball.py
Name:110613024 呂信吾
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

VX = 3
DELAY = 10
GRAVITY = 1
SIZE = 15
REDUCE = 0.9
START_X = 30
START_Y = 40

window = GWindow(800, 500, title='bouncing_ball.py')
oval = GOval(SIZE, SIZE)
num = 0
click = 1


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    window.add(oval, x=START_X, y=START_Y)
    onmouseclicked(start)


def start(mouse):
    vy = 0
    global num, click
    if click != 0:
        if num != 3:
            click = 0
            while True:
                vy += 1
                y = vy + (1/2)*1*GRAVITY
                oval.move(VX, y)
                pause(DELAY)
                if oval.y >= window.height-SIZE:
                    vy = (-vy - 2)*0.9
                if oval.x >= window.width-SIZE+20:
                    window.remove(oval)
                    window.add(oval, x=START_X, y=START_Y)
                    num += 1
                    break
            click += 1


if __name__ == "__main__":
    main()
