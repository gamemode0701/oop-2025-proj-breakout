"""
GAME NAME: BREAKOUT
Game Maker: William Lu, Tony Yu
This code builds a brick-breaking game based on a class 'breakoutgraphics.py'. Each player has NUM_LIVES
lives to break all the bricks. As long as all the bricks are broken or all the lives are used, the game ends.
"""
from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from welcome_screen import WelcomeScreen  # Import the welcome screen
from end_animation import lost_animation, game_over_menu
from ball_powerups import PowerUpManager
from powerup_selector import choose_from_two_powerups

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3           # Number of attempts

def main():
    welcome = WelcomeScreen()  # create once
    while True:
        welcome.show()
        while welcome.level_selected is None:
            pause(100)  # Wait for player to choose

        # Start the game with selected layout
        graphics = BreakoutGraphics(layout_type=welcome.level_selected)
        powerup_manager = PowerUpManager(graphics.window, graphics)
        graphics.extra_balls = []           # Add support attributes
        graphics.slow_timer = 0
        graphics.bomb_mode_timer = 0
        brick_destroyed = 0

        counter = NUM_LIVES
        score = 0
        graphics.board.text = f'Lives: {counter}  Score: {score}'
        graphics.window.add(graphics.board, 0, graphics.window.height - graphics.board.height)

        vx = 0
        vy = 0
        total = graphics.total_bricks

        while counter > 0 and total > 0:
            powerup_manager.update()

            if graphics.slow_timer > 0:
                graphics.slow_timer -= 1
                pause(FRAME_RATE + 5)
            else:
                pause(FRAME_RATE)

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
                brick_destroyed += 1
                powerup_manager.maybe_spawn(graphics.ball.x, graphics.ball.y)
                if brick_destroyed % 10 == 0:
                    chosen = choose_from_two_powerups(graphics.window)
                    powerup_manager.apply_powerup(chosen)
                graphics.board.text = f'Lives: {counter}  Score: {score}'
            elif maybe_brick2 is not None and maybe_brick2 is not graphics.paddle and maybe_brick2 is not graphics.board:
                graphics.window.remove(maybe_brick2)
                vy = -vy
                total -= 1
                score += brick_score(total)
                brick_destroyed += 1
                powerup_manager.maybe_spawn(graphics.ball.x, graphics.ball.y)
                if brick_destroyed % 10 == 0:
                    chosen = choose_from_two_powerups(graphics.window)
                    powerup_manager.apply_powerup(chosen)
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
            pause(2000)
            lost_animation(graphics.window)

        # Ask player what to do next
        action = game_over_menu(graphics.window)
        if action == 'retry':
            graphics.window.close()
            continue  # Restart same level
        elif action == 'menu':
            graphics.window.close()
            continue  # Go back to welcome screen
        else:
            graphics.window.close()
            welcome.window.close()
            break  # Exit game

def brick_score(total):
    if total < 50:
        return 15
    elif total < 20:
        return 20
    else:
        return 10


if __name__ == '__main__':
    main()