import pygame
from constants import COLORS, POWERUPS


class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.visible = True

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)


class Ball(GameObject):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius * 2, radius * 2, color)
        self.radius = radius
        self.dx = 0
        self.dy = 0

    def draw(self, surface):
        if self.visible:
            pygame.draw.circle(surface, self.color, self.rect.center, self.radius)


class Paddle(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.original_width = width
        self.original_height = height


class Brick(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)


class PowerUp(GameObject):
    def __init__(self, x, y, kind):
        config = POWERUPS.get(kind, {'color': 'gray', 'icon': '?'})
        color = COLORS[config['color']]
        self.icon = config['icon']
        super().__init__(x, y, 40, 20, color)
        self.kind = kind
        self.speed = 3
        self.font = pygame.font.SysFont('Segoe UI Emoji', 20)  # 使用支援emoji的字體
        self.label = self.font.render(self.icon, True, COLORS['white'])

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        super().draw(surface)
        if self.visible:
            # 調整圖標位置使其居中
            surface.blit(self.label, (self.rect.x + (self.rect.width - self.label.get_width()) // 2,
                                     self.rect.y + (self.rect.height - self.label.get_height()) // 2))