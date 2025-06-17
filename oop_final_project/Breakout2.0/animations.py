import pygame
import random
import os
from constants import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT


class Animations:
    @staticmethod
    def show_win_animation(screen, big_font, font, clock):
        colors = [COLORS['red'], COLORS['orange'], COLORS['yellow'],
                  COLORS['green'], COLORS['blue'], COLORS['purple'],
                  COLORS['cyan'], COLORS['crimson']]

        # 第一階段：中央閃爍動畫 (2秒)
        center_y = SCREEN_HEIGHT // 2
        for i in range(120):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill(COLORS['black'])
            text = big_font.render("YOU WIN!", True, colors[i % len(colors)])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, center_y))
            screen.blit(text, text_rect)
            pygame.display.flip()
            clock.tick(60)

        # 第二階段：上滑動畫 + 灑花效果同步 (0.5秒)
        target_y = 50
        current_y = center_y
        for i in range(30):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            current_y = current_y - (current_y - target_y) * 0.2
            screen.fill(COLORS['black'])

            text = big_font.render("YOU WIN!", True, COLORS['white'])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, int(current_y)))
            screen.blit(text, text_rect)

            for _ in range(3):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(int(current_y) + 50, SCREEN_HEIGHT)
                color = random.choice(colors)
                pygame.draw.circle(screen, color, (x, y), 3)

            pygame.display.flip()
            clock.tick(60)

        # 第三階段：固定頂部文字 + 持續灑花 (1秒)
        for i in range(60):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill(COLORS['black'])
            text = big_font.render("YOU WIN!", True, COLORS['white'])
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, target_y)))

            for _ in range(5):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(target_y + 50, SCREEN_HEIGHT)
                color = random.choice(colors)
                pygame.draw.circle(screen, color, (x, y), 3)

            pygame.display.flip()
            clock.tick(60)

    @staticmethod
    def show_lose_animation(screen, big_font):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'location.txt')
        coords = []
        x = None

        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith('x') and line[1:].isdigit():
                        x = int(line[1:])
                    elif line.startswith('y') and line[1:].isdigit() and x is not None:
                        y = int(line[1:])
                        coords.append((x, y))
                        x = None
        except FileNotFoundError:
            pass

        if not coords:
            screen.fill(COLORS['black'])
            text = big_font.render("GAME OVER", True, COLORS['crimson'])
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        min_x = min(x for x, _ in coords)
        max_x = max(x for x, _ in coords)
        min_y = min(y for _, y in coords)
        max_y = max(y for _, y in coords)

        art_width = max_x - min_x
        art_height = max_y - min_y

        win_width = screen.get_width()
        win_height = screen.get_height()
        x_offset = (win_width - art_width) // 2 - min_x
        y_offset = (win_height - art_height) // 2 - min_y

        coords = [(x + x_offset, y + y_offset) for x, y in coords]

        screen.fill(COLORS['black'])
        for x, y in coords:
            pygame.draw.rect(screen, COLORS['crimson'], (x, y, 6, 6))
            pygame.display.flip()
            pygame.time.delay(1)

        pygame.time.delay(2000)

        coords_copy = coords[:]
        random.shuffle(coords_copy)
        for x, y in coords_copy:
            pygame.draw.rect(screen, COLORS['black'], (x, y, 6, 6))
            pygame.display.flip()
            pygame.time.delay(2)

        screen.fill(COLORS['black'])
        pygame.display.flip()
        pygame.time.delay(300)