import random
from campy.graphics.gobjects import GRect, GLabel, GOval
from campy.gui.events.timer import pause

class PowerUp:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.label = GLabel(kind)
        self.label.font = '-14'
        self.label.color = 'blue'
        self.x = x
        self.y = y
        self.active = True

    def fall(self, window, speed=3):
        if self.active:
            self.y += speed
            self.label.y = self.y
            self.label.x = self.x
            window.add(self.label)

    def deactivate(self, window):
        self.active = False
        window.remove(self.label)


class PowerUpManager:
    def __init__(self, window, graphics):
        self.window = window
        self.graphics = graphics
        self.powerups = []
        self.active_effects = []

    def maybe_spawn(self, x, y):
        # Chance to spawn a power-up at a given x,y (brick position)
        kinds = ['add_ball', 'multi_ball', 'slow', 'bomb', 'wide_paddle']
        if random.random() < 0.2:  # 20% chance
            kind = random.choice(kinds)
            pu = PowerUp(kind, x, y)
            self.powerups.append(pu)

    def update(self):
        for pu in self.powerups[:]:
            pu.fall(self.window)
            if pu.y > self.window.height:
                self.powerups.remove(pu)
            else:
                if self.graphics.paddle.y <= pu.y + 20 <= self.graphics.paddle.y + self.graphics.paddle.height:
                    if self.graphics.paddle.x <= pu.x <= self.graphics.paddle.x + self.graphics.paddle.width:
                        self.apply_powerup(pu.kind)
                        pu.deactivate(self.window)
                        self.powerups.remove(pu)

    def apply_powerup(self, kind):
        if kind == 'add_ball':
            self.apply_add_ball()
        elif kind == 'multi_ball':
            self.apply_multi_ball()
        elif kind == 'slow':
            self.apply_slow()
        elif kind == 'bomb':
            self.apply_bomb()
        elif kind == 'wide_paddle':
            self.apply_wide_paddle()

    def apply_add_ball(self):
        new_ball = GOval(self.graphics.ball.width, self.graphics.ball.height)
        new_ball.filled = True
        new_ball.fill_color = 'gray'
        self.window.add(new_ball, x=self.graphics.ball.x, y=self.graphics.ball.y)
        # Give it same dx/dy as original
        self.graphics.extra_balls.append({'obj': new_ball, 'dx': self.graphics.get_dx(), 'dy': self.graphics.get_dy()})

    def apply_multi_ball(self):
        for angle in [-3, 0, 3]:
            new_ball = GOval(self.graphics.ball.width, self.graphics.ball.height)
            new_ball.filled = True
            new_ball.fill_color = 'gray'
            self.window.add(new_ball, x=self.graphics.ball.x, y=self.graphics.ball.y)
            self.graphics.extra_balls.append({'obj': new_ball, 'dx': self.graphics.get_dx() + angle, 'dy': self.graphics.get_dy()})

    def apply_slow(self):
        self.graphics.slow_timer = 300  # lasts 300 frames

    def apply_bomb(self):
        self.graphics.bomb_mode_timer = 200

    def apply_wide_paddle(self):
        self.graphics.paddle.width *= 1.5
        pause(5000)
        self.graphics.paddle.width /= 1.5
