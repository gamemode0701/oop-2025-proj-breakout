
import random
import sys
from pygame.locals import *
from constants import *
from game_objects import *
from layouts import Layouts
from animations import Animations


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout (Pygame)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Consolas', 20)
        self.big_font = pygame.font.SysFont('Consolas', 40, bold=True)

        # 將這些初始化移到__init__中
        self.layout_type = 'default'
        self.bomb_radius = BOMB_RADIUS
        self.paddle = None
        self.ball = None
        self.bricks = []
        self.powerups = []
        self.extra_balls = []
        self.lives = 0
        self.score = 0
        self.slow_timer = 0
        self.wide_paddle_timer = 0
        self.bomb_timer = 0
        self.bomb_active = False
        self.penetrate_timer = 0
        self.game_active = False

        # 直接呼叫reset_game進行完整初始化
        self.reset_game()

    def reset_game(self, layout_type=None):
        # 設定或更新布局類型
        if layout_type is not None:
            self.layout_type = layout_type

        # 計算水平居中偏移量
        layout_width = Game.calculate_layout_width(self.layout_type)
        self.layout_offset_x = (SCREEN_WIDTH - layout_width) // 2

        # 初始化遊戲物件
        self.paddle = Paddle(
            (SCREEN_WIDTH - PADDLE_WIDTH) // 2,
            SCREEN_HEIGHT - PADDLE_OFFSET - PADDLE_HEIGHT,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            COLORS['white']
        )

        self.ball = Ball(
            SCREEN_WIDTH // 2 - BALL_RADIUS,
            SCREEN_HEIGHT // 2 - BALL_RADIUS,
            BALL_RADIUS,
            COLORS['white']
        )

        # 重置遊戲狀態
        self.bricks = []
        self.powerups = []
        self.extra_balls = []
        self.lives = NUM_LIVES
        self.score = 0
        self.slow_timer = 0
        self.wide_paddle_timer = 0
        self.bomb_timer = 0
        self.bomb_active = False
        self.penetrate_timer = 0
        self.game_active = False
        if hasattr(self, '_show_win_text'):
            del self._show_win_text

        # 生成磚塊
        self.create_bricks(self.layout_type)

    def create_bricks(self, layout_type):
        """根據布局類型創建磚塊"""
        self.bricks.clear()
        if layout_type == 'test':
            self.bricks = Layouts.layout_test(SCREEN_WIDTH, self.layout_offset_x)
        elif layout_type == 'cross':
            self.bricks = Layouts.layout_default(SCREEN_WIDTH, self.layout_offset_x)
        elif layout_type == 'zigzag':
            self.bricks = Layouts.layout_zigzag(SCREEN_WIDTH, self.layout_offset_x)
        else:
            self.bricks = Layouts.layout_default(SCREEN_WIDTH, self.layout_offset_x)

    def show_welcome_screen(self):
        """顯示歡迎畫面"""
        self.screen.fill(COLORS['black'])
        title = self.big_font.render("BREAKOUT", True, COLORS['white'])
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        options = [
            {"text": "Test Layout (Single Row)", "action": "test"},
            {"text": "Default Layout", "action": "default"},
            {"text": "Zigzag Layout", "action": "zigzag"},
            {"text": "Exit Game", "action": "exit"}
        ]

        buttons = []
        for i, option in enumerate(options):
            btn_rect = pygame.Rect(0, 0, 300, 40)
            btn_rect.center = (SCREEN_WIDTH // 2, 200 + i * 60)

            color = COLORS['red'] if option["action"] == "exit" else COLORS['yellow']
            pygame.draw.rect(self.screen, color, btn_rect)

            text = self.font.render(option["text"], True, COLORS['black'])
            self.screen.blit(text, (btn_rect.centerx - text.get_width() // 2,
                                    btn_rect.centery - text.get_height() // 2))

            buttons.append({"rect": btn_rect, "action": option["action"]})

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "exit":
                                pygame.quit()
                                sys.exit()
                            else:
                                return button["action"]

            # 按鈕懸停效果
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(buttons):
                hover_color = COLORS['crimson'] if button["action"] == "exit" else COLORS['cyan']
                base_color = COLORS['red'] if button["action"] == "exit" else COLORS['yellow']

                if button["rect"].collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, hover_color, button["rect"])
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            if button["action"] == "exit":
                                pygame.quit()
                                sys.exit()
                            else:
                                return button["action"]
                else:
                    pygame.draw.rect(self.screen, base_color, button["rect"])

                text = self.font.render(options[i]["text"], True, COLORS['black'])
                self.screen.blit(text, (button["rect"].centerx - text.get_width() // 2,
                                        button["rect"].centery - text.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self):
        """處理用戶輸入事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and not self.game_active:
                    self.game_active = True
                    self.ball.dx = random.choice([-4, -3, 3, 4])
                    self.ball.dy = INITIAL_Y_SPEED
            elif event.type == MOUSEBUTTONDOWN and not self.game_active:
                self.game_active = True
                self.ball.dx = random.choice([-4, -3, 3, 4])
                self.ball.dy = INITIAL_Y_SPEED

        # 板子控制
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.paddle.rect.x = max(0, self.paddle.rect.x - 8)
        if keys[K_RIGHT]:
            self.paddle.rect.x = min(SCREEN_WIDTH - self.paddle.rect.width, self.paddle.rect.x + 8)

    def update(self):
        """更新遊戲狀態"""
        if not self.game_active:
            return

        # 球移動 (考慮慢速效果)
        speed_factor = 0.5 if self.slow_timer > 0 else 1.0
        if self.slow_timer > 0:
            self.slow_timer -= 1

        # 主球移動
        self.ball.rect.x += int(self.ball.dx * speed_factor)
        self.ball.rect.y += int(self.ball.dy * speed_factor)

        # 額外球移動
        for extra_ball in self.extra_balls[:]:
            extra_ball["rect"].x += int(extra_ball["dx"] * speed_factor)
            extra_ball["rect"].y += int(extra_ball["dy"] * speed_factor)

            # 額外球邊界檢查
            if (extra_ball["rect"].left <= 0 or
                    extra_ball["rect"].right >= self.screen.get_width()):
                extra_ball["dx"] *= -1
            if extra_ball["rect"].top <= 0:
                extra_ball["dy"] *= -1
            if extra_ball["rect"].bottom >= SCREEN_HEIGHT:
                self.extra_balls.remove(extra_ball)
                continue

            # 額外球與板子碰撞
            if extra_ball["rect"].colliderect(self.paddle.rect):
                relative_x = (extra_ball["rect"].centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
                extra_ball["dx"] = int(relative_x * MAX_X_SPEED)
                extra_ball["dy"] = -abs(extra_ball["dy"])

            # 額外球與磚塊碰撞
            for brick in self.bricks[:]:
                if extra_ball["rect"].colliderect(brick.rect):
                    if (extra_ball["rect"].right < brick.rect.left + 5 or
                            extra_ball["rect"].left > brick.rect.right - 5):
                        extra_ball["dx"] *= -1
                    else:
                        extra_ball["dy"] *= -1

                    self.bricks.remove(brick)
                    self.score += self.calculate_brick_score(len(self.bricks))

                    if random.random() < 0.2:
                        self.spawn_powerup(brick.rect.x, brick.rect.y)

                    break

        # 主球邊界碰撞
        if self.ball.rect.left <= 0 or self.ball.rect.right >= self.screen.get_width():
            self.ball.dx *= -1
        if self.ball.rect.top <= 0:
            self.ball.dy *= -1
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over(False)
            else:
                self.reset_ball()
                self.game_active = False

        # 主球與板子碰撞
        if self.ball.rect.colliderect(self.paddle.rect):
            relative_x = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            self.ball.dx = int(relative_x * MAX_X_SPEED)
            self.ball.dy = -abs(self.ball.dy)

        # 主球與磚塊碰撞
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                if self.penetrate_timer > 0:
                    self.bricks.remove(brick)
                    self.score += self.calculate_brick_score(len(self.bricks))
                    if random.random() < 0.2:
                        self.spawn_powerup(brick.rect.x, brick.rect.y)
                    continue

                if (self.ball.rect.right < brick.rect.left + 5 or
                        self.ball.rect.left > brick.rect.right - 5):
                    self.ball.dx *= -1
                else:
                    self.ball.dy *= -1

                if self.bomb_active:
                    self.trigger_bomb_effect(brick.rect.centerx, brick.rect.centery)
                else:
                    self.bricks.remove(brick)
                    self.score += self.calculate_brick_score(len(self.bricks))

                if random.random() < 0.2:
                    self.spawn_powerup(brick.rect.x, brick.rect.y)

                break

        # 道具更新
        for powerup in self.powerups[:]:
            powerup.update()

            if powerup.rect.colliderect(self.paddle.rect):
                self.apply_powerup(powerup.kind)
                self.powerups.remove(powerup)
            elif powerup.rect.top > SCREEN_HEIGHT:
                self.powerups.remove(powerup)

        # 寬板計時器
        if self.wide_paddle_timer > 0:
            self.wide_paddle_timer -= 1
            if self.wide_paddle_timer == 0:
                self.paddle.rect.width = self.paddle.original_width
                self.paddle.rect.x = min(max(self.paddle.rect.x, 0),
                                         SCREEN_WIDTH - self.paddle.rect.width)

        # 炸彈計時器
        if self.bomb_timer > 0:
            self.bomb_timer -= 1
            if self.bomb_timer == 0:
                self.bomb_active = False

        # 穿透技能計時器
        if self.penetrate_timer > 0:
            self.penetrate_timer -= 1

        # 勝利條件檢查
        if len(self.bricks) == 0:
            self.game_over(True)

    def trigger_bomb_effect(self, center_x, center_y):
        """觸發炸彈效果"""
        bricks_to_remove = []

        for brick in self.bricks[:]:
            distance = ((brick.rect.centerx - center_x) ** 2 +
                        (brick.rect.centery - center_y) ** 2) ** 0.5
            if distance <= self.bomb_radius:
                bricks_to_remove.append(brick)

        for brick in bricks_to_remove:
            if brick in self.bricks:
                self.bricks.remove(brick)
                self.score += self.calculate_brick_score(len(self.bricks))

        # 視覺效果
        particle_colors = [COLORS['red'], COLORS['orange']]
        particles = []
        for _ in range(120):
            angle = random.uniform(0, 2 * 3.14159)
            radius = random.uniform(0, self.bomb_radius)
            px = int(center_x + radius * math.cos(angle))
            py = int(center_y + radius * math.sin(angle))
            color = random.choice(particle_colors)
            size = random.randint(3, 7)
            particles.append((px, py, color, size))

        for _ in range(15):
            self.draw()
            for px, py, color, size in particles:
                pygame.draw.circle(self.screen, color, (px, py), size)
            pygame.display.flip()
            pygame.time.delay(20)

    def calculate_brick_score(self, bricks_left):
        """計算磚塊分數"""
        if bricks_left < 20:
            return 20
        elif bricks_left < 50:
            return 15
        else:
            return 10

    def spawn_powerup(self, x, y):
        """生成道具"""
        kinds = ['add_ball', 'multi_ball', 'slow', 'bomb', 'wide_paddle', 'penetrate']
        powerup = PowerUp(x, y, random.choice(kinds))
        self.powerups.append(powerup)

    def apply_powerup(self, kind):
        """應用道具效果"""
        if kind == 'wide_paddle':
            self.paddle.rect.width = int(self.paddle.original_width * 1.5)
            self.paddle.rect.x = min(max(self.paddle.rect.x, 0),
                                     SCREEN_WIDTH - self.paddle.rect.width)
            self.wide_paddle_timer = FPS * 10

        elif kind == 'slow':
            # 減速技能
            self.slow_timer = FPS * 10

        elif kind == 'add_ball':
            # 生成一個與主球不同角度的額外球
            angle = random.choice([-4, -2, 2, 4])
            self.add_extra_ball(angle)

        elif kind == 'multi_ball':
            # 生成三個額外球，角度分散且不與主球重疊
            angles = [-5, -3, -2, 2, 3, 5]  # 可選角度
            selected_angles = random.sample(angles, 3)  # 隨機選擇三個不同角度
            for angle in selected_angles:
                self.add_extra_ball(angle)

        elif kind == 'bomb':
            self.bomb_active = True
            self.bomb_timer = FPS * 3

        elif kind == 'penetrate':
            self.penetrate_timer = FPS * 3

    def add_extra_ball(self, angle=0):
        """添加額外球"""
        new_ball = {
            "rect": pygame.Rect(self.ball.rect.x, self.ball.rect.y,
                                BALL_RADIUS * 2, BALL_RADIUS * 2),
            "dx": self.ball.dx + angle,
            "dy": self.ball.dy,
            "color": COLORS['gray'],
            "radius": EXTRA_BALL_RADIUS
        }
        self.extra_balls.append(new_ball)

    def reset_ball(self):
        """重置球位置"""
        self.ball.rect.center = (self.screen.get_width() // 2, SCREEN_HEIGHT // 2)
        self.ball.dx = 0
        self.ball.dy = 0
        self.game_active = False

    def game_over(self, won):
        """遊戲結束處理"""
        self.game_active = False
        self._show_win_text = won

        if won:
            Animations.show_win_animation(self.screen, self.big_font, self.font, self.clock)
        else:
            Animations.show_lose_animation(self.screen, self.big_font)

        action = self.show_game_over_menu()

        if action == 'retry':
            self.reset_game()
        elif action == 'next_level':
            self.layout_type = self.get_next_layout()
            self.reset_game(self.layout_type)
        elif action == 'menu':
            self.layout_type = self.show_welcome_screen()
            self.reset_game()
        else:
            pygame.quit()
            sys.exit()

    def get_next_layout(self):
        """獲取下一關布局"""
        layouts = ['test', 'default', 'zigzag']
        current_index = layouts.index(self.layout_type) if self.layout_type in layouts else 0
        next_index = (current_index + 1) % len(layouts)
        return layouts[next_index]

    def show_game_over_menu(self):
        """顯示遊戲結束選單"""
        if hasattr(self, '_show_win_text') and self._show_win_text:
            options = ['next_level', 'menu', 'exit']
        else:
            options = ['retry', 'menu', 'exit']

        selected = 0
        option_rects = []

        while True:
            self.screen.fill(COLORS['black'])

            # 顯示遊戲結果標題
            if hasattr(self, '_show_win_text') and self._show_win_text:
                result_text = self.big_font.render("YOU WIN!", True, COLORS['green'])
            else:
                result_text = self.big_font.render("GAME OVER", True, COLORS['red'])

            self.screen.blit(result_text,
                             (SCREEN_WIDTH // 2 - result_text.get_width() // 2, 50))

            # 顯示分數
            score_text = self.font.render(f"Final Score: {self.score}", True, COLORS['white'])
            self.screen.blit(score_text,
                             (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 120))

            # 繪製選項按鈕
            option_rects = []
            for i, option in enumerate(options):
                mouse_pos = pygame.mouse.get_pos()
                is_hovered = False

                if option == 'next_level':
                    display_text = "NEXT LEVEL"
                elif option == 'retry':
                    display_text = "RETRY"
                else:
                    display_text = option.upper()

                btn_rect = pygame.Rect(0, 0, 200, 40)
                btn_rect.center = (SCREEN_WIDTH // 2, 200 + i * 70)

                is_hovered = btn_rect.collidepoint(mouse_pos)
                if is_hovered:
                    selected = i

                if option == 'exit':
                    color = COLORS['yellow'] if (i == selected or is_hovered) else COLORS['#b22222']
                else:
                    color = COLORS['yellow'] if (i == selected or is_hovered) else COLORS['white']

                pygame.draw.rect(self.screen, color, btn_rect)

                text = self.font.render(display_text, True, COLORS['black'])
                self.screen.blit(text,
                                 (btn_rect.centerx - text.get_width() // 2,
                                  btn_rect.centery - text.get_height() // 2))

                option_rects.append(btn_rect)

            pygame.display.flip()

            # 事件處理
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == K_RETURN:
                        return options[selected]
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(mouse_pos):
                            return options[i]
                elif event.type == MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(mouse_pos):
                            selected = i

            self.clock.tick(FPS)

    def draw(self):
        """繪製遊戲畫面"""
        self.screen.fill(COLORS['black'])

        # 如果勝利且處於選單狀態，繪製YOU WIN!文字
        if hasattr(self, '_show_win_text') and self._show_win_text:
            text = self.big_font.render("YOU WIN!", True, COLORS['white'])
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        # 繪製所有磚塊
        for brick in self.bricks:
            brick.draw(self.screen)

        # 繪製板子
        self.paddle.draw(self.screen)

        # 繪製球
        self.ball.draw(self.screen)
        for extra_ball in self.extra_balls:
            pygame.draw.circle(self.screen, extra_ball["color"],
                               extra_ball["rect"].center, EXTRA_BALL_RADIUS)

        # 繪製道具
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # 繪製分數和生命
        score_text = self.font.render(f'Score: {self.score} Lives: {self.lives}', True, COLORS['white'])
        self.screen.blit(score_text, (10, 10))

        # 如果遊戲未開始，顯示提示
        if not self.game_active and self.ball.dx == 0 and self.ball.dy == 0:
            prompt = self.font.render("Press SPACE or Click to Start", True, COLORS['white'])
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2,
                                      SCREEN_HEIGHT - 50))

        # 顯示特殊技能狀態
        if self.bomb_timer > 0:
            bomb_text = self.font.render("BOMB ACTIVE!", True, COLORS['red'])
            self.screen.blit(bomb_text, (SCREEN_WIDTH // 2 - bomb_text.get_width() // 2, 30))
        if self.penetrate_timer > 0:
            penetrate_text = self.font.render("PENETRATE ACTIVE!", True, COLORS['magenta'])
            self.screen.blit(penetrate_text, (SCREEN_WIDTH // 2 - penetrate_text.get_width() // 2, 60))

        pygame.display.flip()

    def run(self):
        """主遊戲循環"""
        while True:
            selected = self.show_welcome_screen()
            self.reset_game(selected)

            # 等待玩家開始遊戲
            waiting = True
            while waiting:
                self.handle_events()
                self.draw()
                if self.game_active:
                    waiting = False
                self.clock.tick(FPS)

            # 主遊戲循環
            while self.lives > 0 and len(self.bricks) > 0:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)

    @staticmethod
    def calculate_layout_width(layout_type):
        """計算每種布局需要的最小寬度"""
        if layout_type == 'default':
            return BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING) - BRICK_SPACING
        elif layout_type == 'test':
            return BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING)
        elif layout_type == 'zigzag':
            return int((BRICK_COLS + 0.5) * (BRICK_WIDTH + BRICK_SPACING))
        return SCREEN_WIDTH
