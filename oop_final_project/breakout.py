"""
GAME NAME: BREAKOUT
Game Maker: William Lu, Tony Yu
This code build a brick breaking game, based on a class 'breakoutgraphics.py', and every player had NUM_LIVES
lives to break all the bricks. As long as all the bricks are broken, or all the lives is used, the game is over.
"""
from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from welcome_screen import WelcomeScreen  # Import the welcome screen
from end_animation import lost_animation

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3           # Number of attempts
counter = NUM_LIVES     # Record the lives remaining
score = 0               # Record the score


def main():
    global counter, score

    # Show welcome screen
    welcome = WelcomeScreen()
    while welcome.level_selected is None:
        pause(100)  # Important: keep GUI responsive

    # Start the game with selected layout
    graphics = BreakoutGraphics(layout_type=welcome.level_selected)

    graphics.board.text = f'Lives: {counter}  Score: {score}'
    graphics.window.add(graphics.board, 0, graphics.window.height - graphics.board.height)

    vx = 0
    vy = 0
    total = graphics.total_bricks

    while counter > 0 and total > 0:
        if vx == vy == 0:
            vx = graphics.get_dx()
            vy = graphics.get_dy()
        graphics.ball.move(vx, vy)

        if graphics.ball.x >= graphics.window.width or graphics.ball.x <= 0:
            vx = -vx
        if graphics.ball.y <= 0:
            vy = -vy
        if graphics.ball.y >= graphics.window.height:
            graphics.reset_ball()
            vx = 0
            vy = 0
            counter -= 1
            graphics.board.text = f'Lives: {counter}  Score: {score}'

        if total >= 50:
            pause(FRAME_RATE)
        elif total >= 20:
            pause(FRAME_RATE - 2)
        else:
            pause(FRAME_RATE - 4)

        maybe_brick1 = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y)
        maybe_brick2 = graphics.window.get_object_at(graphics.ball.x + graphics.ball.width, graphics.ball.y)
        maybe_paddle1 = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y + graphics.ball.height)
        maybe_paddle2 = graphics.window.get_object_at(graphics.ball.x + graphics.ball.width,
                                                      graphics.ball.y + graphics.ball.height)

        if maybe_brick1 is not None and maybe_brick1 is not graphics.paddle and maybe_brick1 is not graphics.board:
            graphics.window.remove(maybe_brick1)
            vy = -vy
            total -= 1
            score += brick_score(total)
            graphics.board.text = f'Lives: {counter}  Score: {score}'
        elif maybe_brick2 is not None and maybe_brick2 is not graphics.paddle and maybe_brick2 is not graphics.board:
            graphics.window.remove(maybe_brick2)
            vy = -vy
            total -= 1
            score += brick_score(total)
            graphics.board.text = f'Lives: {counter}  Score: {score}'
        elif maybe_paddle1 is graphics.paddle or maybe_paddle2 is graphics.paddle:
            vy = -vy

    finish_board = graphics.finish
    if counter > 0 and total <= 0:
        finish_board.text = 'Congratulations!!'
        graphics.window.add(finish_board, x=(graphics.window.width - finish_board.width) / 2,
                        y=(graphics.window.height + finish_board.height) / 2)
        pause(2000)

    else:
        graphics.window.remove(graphics.ball)
        finish_board.text = 'Game Over...'
        graphics.window.add(finish_board, x=(graphics.window.width - finish_board.width) / 2,
                        y=(graphics.window.height + finish_board.height) / 2)
        pause(2000) #let player see the game over message
        lost_animation(graphics.window)

def brick_score(total):
    if total < 50:
        return 15
    elif total < 20:
        return 20
    else:
        return 10


if __name__ == '__main__':
    main()
