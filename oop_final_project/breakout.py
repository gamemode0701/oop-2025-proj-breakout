"""
GAME NAME: BREAKOUT
Game Maker: William Lu, Tony Yu
This code builds a brick-breaking game based on a class 'breakoutgraphics.py'. Each player has NUM_LIVES
lives to break all the bricks. As long as all the bricks are broken or all the lives are used, the game ends.
"""
from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from welcome_screen import WelcomeScreen  # 匯入歡迎畫面
from end_animation import lost_animation, game_over_menu
from ball_powerups import PowerUpManager
from powerup_selector import choose_from_two_powerups
from paddle_manager import PaddleManager

FRAME_RATE = 10         # 每幀間隔（數值越小速度越快）
NUM_LIVES = 3           # 玩家生命數

def main():
    welcome = WelcomeScreen()  # 建立歡迎畫面，只建立一次
    while True:
        welcome.show()  # 顯示歡迎畫面，等待玩家選擇
        while welcome.level_selected is None:
            pause(100)  # 等待玩家選擇關卡或退出

        # 根據玩家選擇的關卡建立遊戲畫面
        graphics = BreakoutGraphics(layout_type=welcome.level_selected)
        paddle_manager = PaddleManager(graphics.paddle)
        graphics.paddle_manager = paddle_manager 
        powerup_manager = PowerUpManager(graphics.window, graphics)  # 建立道具管理器
        graphics.extra_balls = []           # 額外球的屬性
        graphics.slow_timer = 0             # 慢速道具計時器
        graphics.wide_paddle_timer = 0      # 寬板道具計時器
        graphics.bomb_mode_timer = 0        # 炸彈模式計時器
        brick_destroyed = 0                 # 已消除磚塊數

        counter = NUM_LIVES                 # 剩餘生命
        score = 0                           # 分數
        graphics.board.text = f'Lives: {counter}  Score: {score}'  # 顯示生命與分數
        graphics.window.add(graphics.board, 0, graphics.window.height - graphics.board.height)  # 加到底部
        powerup_kind = ''  # 初始道具類型


        vx = 0      # 球的水平速度
        vy = 0      # 球的垂直速度
        total = graphics.total_bricks  # 剩餘磚塊數

        # 遊戲主迴圈：只要還有生命且還有磚塊
        while counter > 0 and total > 0:
            powerup_manager.update()  # 更新道具狀態
            # 檢查是否有道具掉落到板子上
            for maybe_powerup in [
                graphics.window.get_object_at(graphics.paddle.x, graphics.ball.y),
                graphics.window.get_object_at(graphics.paddle.x + graphics.paddle.width, graphics.ball.y),
                graphics.window.get_object_at(graphics.paddle.x + graphics.paddle.width / 2, graphics.ball.y)
            ]:
                if (
                    maybe_powerup is not None
                    and maybe_powerup is not graphics.ball
                    and maybe_powerup is not graphics.board
                    and hasattr(maybe_powerup, 'powerup_ref')
                ):
                    powerup_obj = maybe_powerup.powerup_ref
                    powerup_kind = powerup_obj.kind
                    powerup_manager.apply_powerup(powerup_kind)
                    powerup_obj.deactivate(graphics.window)
                    if powerup_obj in powerup_manager.powerups:
                        powerup_manager.powerups.remove(powerup_obj)

            # 慢速道具效果
            if graphics.slow_timer > 0:
                graphics.slow_timer -= 1
                pause(FRAME_RATE + 5)  # 慢速時延長暫停時間
            else:
                pause(FRAME_RATE)

            # 寬板道具效果
            if graphics.wide_paddle_timer > 0:
                graphics.wide_paddle_timer -= 1
                # Effect is already applied, just wait for timer to end
                if graphics.wide_paddle_timer == 0:
                    graphics.paddle_manager.restore()

            # 炸彈道具效果
            if graphics.bomb_mode_timer > 0:
                graphics.bomb_mode_timer -= 1
                # Add bomb effect logic here if needed

            # 若球尚未發射，取得初始速度
            if vx == vy == 0:
                vx = graphics.get_dx()
                vy = graphics.get_dy()
            graphics.ball.move(vx, vy)  # 移動球

            # 球碰到左右牆反彈
            if graphics.ball.x >= graphics.window.width or graphics.ball.x <= 0:
                vx = -vx
            # 球碰到上方牆反彈
            if graphics.ball.y <= 0:
                vy = -vy
            # 球掉到下方，重設球並扣一條命
            if graphics.ball.y >= graphics.window.height:
                graphics.reset_ball()
                vx = 0
                vy = 0
                counter -= 1
                graphics.board.text = f'Lives: {counter}  Score: {score}'

            # 根據剩餘磚塊數調整速度
            if total >= 50:
                pause(FRAME_RATE)
            elif total >= 20:
                pause(FRAME_RATE - 2)
            else:
                pause(FRAME_RATE - 4)

            # 檢查球的四個角是否碰到物件
            maybe_brick1 = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y)  # 左上角
            maybe_brick2 = graphics.window.get_object_at(graphics.ball.x + graphics.ball.width, graphics.ball.y)  # 右上角
            maybe_paddle1 = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y + graphics.ball.height)  # 左下角
            maybe_paddle2 = graphics.window.get_object_at(graphics.ball.x + graphics.ball.width,
                                                          graphics.ball.y + graphics.ball.height)  # 右下角

            # 球碰到磚塊1（左上角）
            if maybe_brick1 is not None and maybe_brick1 is not graphics.paddle and maybe_brick1 is not graphics.board:
                graphics.window.remove(maybe_brick1)  # 移除磚塊
                vy = -vy  # 反彈
                total -= 1  # 剩餘磚塊減一
                score += brick_score(total)  # 加分
                brick_destroyed += 1  # 已消除磚塊數加一
                # 檢查是否產生道具
                powerup_manager.maybe_spawn(graphics.ball.x, graphics.ball.y)
                if brick_destroyed % 10 == 0:
                    chosen = choose_from_two_powerups(graphics.window)  # 每10塊選擇一個道具
                    powerup_manager.apply_powerup(chosen)
                graphics.board.text = f'Lives: {counter}  Score: {score}'
            # 球碰到磚塊2（右上角）
            elif maybe_brick2 is not None and maybe_brick2 is not graphics.paddle and maybe_brick2 is not graphics.board:
                graphics.window.remove(maybe_brick2)  # 移除磚塊
                vy = -vy  # 反彈
                total -= 1  # 剩餘磚塊減一
                score += brick_score(total)  # 加分
                brick_destroyed += 1  # 已消除磚塊數加一
                powerup_manager.maybe_spawn(graphics.ball.x, graphics.ball.y)  # 檢查是否產生道具
                if brick_destroyed % 10 == 0:
                    chosen = choose_from_two_powerups(graphics.window)  # 每10塊選擇一個道具
                    powerup_manager.apply_powerup(chosen)
                graphics.board.text = f'Lives: {counter}  Score: {score}'
            # 球碰到板子反彈
            elif maybe_paddle1 is graphics.paddle or maybe_paddle2 is graphics.paddle:
                vy = -vy  # 球碰到板子時反彈

        # 遊戲結束，顯示結束訊息
        finish_board = graphics.finish
        if counter > 0 and total <= 0:
            finish_board.text = 'Congratulations!!'  # 通關訊息
            graphics.window.add(finish_board, x=(graphics.window.width - finish_board.width) / 2,
                                y=(graphics.window.height + finish_board.height) / 2)
            pause(2000)
        else:
            pause(200)
            lost_animation(graphics.window)  # 失敗動畫

        # 遊戲結束後詢問玩家下一步
        action = game_over_menu(graphics.window)
        if action == 'retry':
            graphics.window.close()
            continue  # 重新開始同一關
        elif action == 'menu':
            graphics.window.close()
            continue  # 回到主選單
        else:
            graphics.window.close()
            welcome.window.close()
            break  # 離開遊戲

def brick_score(total):
    """根據剩餘磚塊數決定每塊磚的分數"""
    if total < 50:
        return 15
    elif total < 20:
        return 20
    else:
        return 10

if __name__ == '__main__':
    main()