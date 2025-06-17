def ball_motion(graphics):
    """
    控制場上所有球的移動與邊界反彈。
    只有當球速度不為 0 時才移動球。
    """
    dx = graphics.get_dx()
    dy = graphics.get_dy()
    if dx == 0 and dy == 0:
        return  # 球尚未發射

    ball = graphics.ball
    ball.move(dx, dy)

    # 左右牆反彈
    if ball.x >= graphics.window.width or ball.x <= 0:
        graphics._BreakoutGraphics__dx = -dx
    # 上牆反彈
    if ball.y <= 0:
        graphics._BreakoutGraphics__dy = -dy
    # 下方出界
    if ball.y >= graphics.window.height:
        graphics.reset_ball()
        graphics._BreakoutGraphics__dx = 0
        graphics._BreakoutGraphics__dy = 0

    # 額外球同理（略，可依需求補上）