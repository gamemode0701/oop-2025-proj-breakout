"""
File: clear_bricks.py
Name:110613024 呂信吾
---------------------------------
TODO:
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GRect, GLabel
from campy.gui.events.mouse import onmouseclicked
from campy.gui.events.timer import pause
import random

END_ANIMATION = 'ON'
# Optional, insert 'ON' to activate the animation when losing the game

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
DELAY = 10
SIZE = 30
MIN_Y_SPEED = 2
MAX_Y_SPEED = 5
window = GWindow(WINDOW_WIDTH, WINDOW_HEIGHT)
brick = GRect(SIZE, SIZE)
brick.filled = True
brick.fill_color = 'black'
target = 0
fail = 0


def main():
    """
    Thw main function of this game.
    """
    global fail
    onmouseclicked(clear)
    spawn_brick()
    if fail == 3:
        if END_ANIMATION == 'ON':
            animation()


def clear(mouse):
    """
    To delete the brick when being clicked.
    """
    global target
    if brick.x <= mouse.x <= brick.x+SIZE and brick.y <= mouse.y <= brick.y+SIZE:
        window.remove(brick)
        target = 0


def spawn_brick():
    """
    to spawn a falling brick with random speed.
    """
    global target, fail
    while True:
        if target == 0:
            fall_speed = random.randint(MIN_Y_SPEED, MAX_Y_SPEED + 1)
            window.add(brick, x=random.randint(0, window.width-SIZE-1), y=0)
            target += 1
        while target != 0:
            brick.move(0, fall_speed)
            pause(DELAY)
            if brick.y >= window.height:
                target -= 1
                fail += 1
                break
        if fail == 3:
            break


def animation():
    """
    To display a 'game over' animation when the player lost.
    """
    cord = 0
    clean = 0
    with open('location.txt', 'r') as f:
        for line in f:
            if cord == 2:
                pixel = GRect(6, 6)
                pixel.filled = True
                pixel.fill_color = 'crimson'
                window.add(pixel, x=x, y=y)
                pause(1)
                cord = 0
            if line.find('x') != -1:
                cord_x = line[1:]
                x = int(cord_x)
                cord += 1
            if line.find('y') != -1:
                cord_y = line[1:]
                y = int(cord_y)
                cord += 1
        if cord == 2:
            pixel = GRect(6, 6)
            pixel.filled = True
            pixel.fill_color = 'crimson'
            window.add(pixel, x=x, y=y)
            cord = 0
    pause(3000)
    while True:
        x = random.randint(50, 454)
        y = random.randint(221, 274)
        fade = window.get_object_at(x, y)
        if fade is not None:
            window.remove(fade)
            clean += 1
            if clean >= 381:
                break
            pause(2)


if __name__ == '__main__':
    main()