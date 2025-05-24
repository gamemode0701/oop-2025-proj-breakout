"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10      # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # 7Initial vertical speed for the ball
MAX_X_SPEED = 5       # 5Maximum initial horizontal speed for the ball


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):
        # Creating the elements
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.ball_radius = ball_radius
        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)
        # Create a paddle
        self.window.add(self.paddle, x=(window_width-paddle_width)/2, y=window_height-paddle_offset)
        # Center a filled ball in the graphical window
        self.window.add(self.ball, x=(window_width-ball_radius)/2, y=(window_height-ball_radius)/2)
        # Draw bricks
        self.color_list = ['red', 'red', 'orange', 'orange', 'yellow', 'yellow', 'green', 'green', 'blue', 'blue']
        for j in range(brick_cols):
            for i in range(brick_rows):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.brick.fill_color = self.color_list[i % 10]
                self.window.add(self.brick, x=j*(brick_width+brick_spacing),
                                y=brick_offset+i*(brick_height+brick_spacing))
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        # Initialize our mouse listeners
        onmousemoved(self.follow)
        onmouseclicked(self.ball_movement)

    # methods
    def follow(self, mouse):
        # when paddle.x < mouse.x
        if self.paddle.x <= self.window.width-PADDLE_WIDTH:
            while self.paddle.x+PADDLE_WIDTH/2 < mouse.x:
                self.paddle.move(1, 0)
        # when paddle.x > mouse.x
        if 0 <= self.paddle.x:
            while self.paddle.x+PADDLE_WIDTH/2 > mouse.x:
                self.paddle.move(-1, 0)
        # Default initial velocity for the ball
        # Initialize our mouse listeners

    def reset_ball(self):
        self.__dx = 0
        self.__dy = 0

    def ball_movement(self, event):
        if self.__dx == 0:
            self.__dx = random.randint(1, MAX_X_SPEED+1)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def get_dx(self):
        # return x velocity of ball to the user
        return self.__dx, self.__dy

    def get_obj_info(self):
        return self.window, self.ball, self.ball_radius, self.paddle, BRICK_HEIGHT, BRICK_COLS, BRICK_ROWS

    

