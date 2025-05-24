"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts

game_in_progress = False


def main():
    chance = 3
    graphics = BreakoutGraphics()
    window, ball, ball_radius, paddle, brick_height, cols, rows = graphics.get_obj_info()
    ball_center_x, ball_center_y = ball.x+ball_radius, ball.y+ball_radius
    vx, vy = 0, 0
    brick_num = cols*rows
    # Add the animation loop here!
    while chance > 0 and cols*rows != 0:
        if chance == 0 or brick_num == 0:
            break
        # only when the ball is at center and not moving will vx and vy be reset(to make mouseclick useless during game)
        if vx == 0 and vy == 0:
            vx, vy = graphics.get_dx()
        # if not game_in_progress:
        ball.move(vx, vy)
        if ball.x <= 0 or ball.x+2*ball_radius >= window.width:
            vx = -vx
        if ball.y <= 0:
            vy = -vy
        if ball.y >= window.height:
            window.remove(ball)
            window.add(ball, x=(window.width-ball_radius)/2, y=(window.height-ball_radius)/2)
            vx, vy = 0, 0
            graphics.reset_ball()
            chance -= 1
        # to check if the ball hits anything
        target1 = window.get_object_at(ball.x, ball.y)
        target2 = window.get_object_at(ball.x+2*ball_radius, ball.y)
        target3 = window.get_object_at(ball.x, ball.y+2*ball_radius)
        target4 = window.get_object_at(ball.x+2*ball_radius, ball.y+2*ball_radius)
        scan = 0
        if target1 is not None:
            if target1 is paddle:
                vy = -vy
            else:
                if target1.y + brick_height >= ball_center_y >= target1.y:
                    vx = -vx
                else:
                    vy = -vy
                window.remove(target1)
                brick_num -= 1
        elif target2 is not None:
            if target2 is paddle:
                vy = -vy
            else:
                if target2.y + brick_height >= ball_center_y >= target2.y:
                    vx = -vx
                else:
                    vy = -vy
                window.remove(target2)
                brick_num -= 1
        elif target3 is not None:
            if target3 is paddle:
                vy = -vy
            else:
                if target3.y + brick_height >= ball_center_y >= target3.y:
                    vx = -vx
                else:
                    vy = -vy
                window.remove(target3)
                brick_num -= 1
        elif target4 is not None:
            if target4 is paddle:
                vy = -vy
            else:
                if target4.y + brick_height >= ball_center_y >= target4.y:
                    vx = -vx
                else:
                    vy = -vy
                window.remove(target4)
                brick_num -= 1
        pause(FRAME_RATE)





if __name__ == '__main__':
    main()
