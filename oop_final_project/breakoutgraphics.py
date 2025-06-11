"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
name: Tony Yu
This program create a class which will be used by breakout.py, and will make a brick breaking game
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5
BRICK_WIDTH = 40
BRICK_HEIGHT = 15
BRICK_ROWS = 10
BRICK_COLS = 10
BRICK_OFFSET = 50
BALL_RADIUS = 10
PADDLE_WIDTH = 75
PADDLE_HEIGHT = 15
PADDLE_OFFSET = 50
INITIAL_Y_SPEED = 5
MAX_X_SPEED = 5
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 15
                    

class BreakoutGraphics:
    def __init__(self, layout_type='default', **kwargs):
        self.brick_rows = kwargs.get('brick_rows', BRICK_ROWS)
        self.brick_cols = kwargs.get('brick_cols', BRICK_COLS)
        self.brick_width = kwargs.get('brick_width', BRICK_WIDTH)
        self.brick_height = kwargs.get('brick_height', BRICK_HEIGHT)
        self.brick_spacing = kwargs.get('brick_spacing', BRICK_SPACING)
        self.brick_offset = kwargs.get('brick_offset', BRICK_OFFSET)
        paddle_width = kwargs.get('paddle_width', PADDLE_WIDTH)
        paddle_height = kwargs.get('paddle_height', PADDLE_HEIGHT)
        paddle_offset = kwargs.get('paddle_offset', PADDLE_OFFSET)
        ball_radius = kwargs.get('ball_radius', BALL_RADIUS)
        self.extra_balls = []
        self.slow_timer = 0
        self.bomb_mode_timer = 0


        window_width = self.brick_cols * (self.brick_width + self.brick_spacing) - self.brick_spacing
        window_height = self.brick_offset + 3 * (self.brick_rows * (self.brick_height + self.brick_spacing) - self.brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title='Breakout')

        self.paddle = GRect(width=paddle_width, height=paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(window_width - paddle_width) / 2, y=window_height - paddle_offset - paddle_height)

        self.ball = GOval(ball_radius, ball_radius)
        self.ball.filled = True
        self.window.add(self.ball, x=(self.window.width - ball_radius) / 2, y=(self.window.height - ball_radius) / 2)

        self.__dx = 0
        self.__dy = 0

        onmousemoved(self.track)
        onmouseclicked(self.start)

        self.bricks = []
        self.total_bricks = 0
        self.board = GLabel(' ')
        self.finish = GLabel(' ')

        self.build_bricks(layout_type)

    def build_bricks(self, layout_type):
        if layout_type == 'default':
            self.layout_default()
        elif layout_type == 'cross':
            self.layout_cross()
        elif layout_type == 'zigzag':
            self.layout_zigzag()
        else:
            self.layout_default()

    def add_brick(self, i, j, color):
        x = j * (self.brick_width + self.brick_spacing)
        y = i * (self.brick_height + self.brick_spacing) + self.brick_offset
        brick = GRect(self.brick_width, self.brick_height)
        brick.filled = True
        brick.fill_color = color
        brick.color = color
        self.window.add(brick, x=x, y=y)
        self.bricks.append(brick)
        self.total_bricks += 1

    def get_color_by_row(self, i):
        if i < 2:
            return 'red'
        elif i < 4:
            return 'orange'
        elif i < 6:
            return 'yellow'
        elif i < 8:
            return 'green'
        else:
            return 'blue'

    def layout_default(self):
        for i in range(self.brick_rows):
            for j in range(self.brick_cols):
                color = self.get_color_by_row(i)
                self.add_brick(i, j, color)

    def layout_cross(self):
        mid_r = self.brick_rows // 2
        mid_c = self.brick_cols // 2
        for i in range(self.brick_rows):
            for j in range(self.brick_cols):
                if i == mid_r or j == mid_c:
                    color = self.get_color_by_row(i)
                    self.add_brick(i, j, color)

    def layout_zigzag(self):
        for i in range(self.brick_rows):
            offset = 0 if i % 2 == 0 else self.brick_width // 2
            for j in range(self.brick_cols):
                color = self.get_color_by_row(i)
                x = j * (self.brick_width + self.brick_spacing) + offset
                y = i * (self.brick_height + self.brick_spacing) + self.brick_offset
                brick = GRect(self.brick_width, self.brick_height)
                brick.filled = True
                brick.fill_color = color
                brick.color = color
                self.window.add(brick, x=x, y=y)
                self.bricks.append(brick)
                self.total_bricks += 1

    def track(self, event):
        if self.paddle.width//2 < event.x < self.window.width-self.paddle.width//2:
            self.paddle.x = event.x - PADDLE_WIDTH//2
        elif event.x < self.paddle.width//2:
            self.paddle.x = 0
        else:
            self.paddle.x = self.window.width-self.paddle.width

    def start(self, _):
        if self.__dx == 0:
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() < 0.5:
                self.__dx = -self.__dx
            self.__dy = INITIAL_Y_SPEED

    def reset_ball(self):
        self.window.remove(self.ball)
        self.__dx = 0
        self.__dy = 0
        self.window.add(self.ball, x=(self.window.width - self.ball.width) / 2,
                        y=(self.window.height - self.ball.height) / 2)

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

if __name__ == '__main__':
    welcome = WelcomeScreen()
    while welcome.level_selected is None:
        pass
    graphics = BreakoutGraphics(layout_type=welcome.level_selected)
