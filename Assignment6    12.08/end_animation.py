from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

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