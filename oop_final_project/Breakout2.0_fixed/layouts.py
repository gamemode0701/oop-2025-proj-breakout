from constants import COLORS, BRICK_ROWS, BRICK_COLS, BRICK_WIDTH, BRICK_HEIGHT, BRICK_SPACING, BRICK_OFFSET, \
    BRICK_COLORS
from game_objects import Brick


class Layouts:
    @staticmethod
    def get_color_by_row(row):
        color_name = BRICK_COLORS.get(row // 2 * 2, 'blue')  # 默認藍色
        return COLORS[color_name]

    @staticmethod
    def layout_test(screen_width, layout_offset_x):  # 新增：簡化的測試布局
        bricks = []
        # 只在第5行生成一排磚塊 (方便測試)
        row = 5
        for col in range(BRICK_COLS):
            x = layout_offset_x + col * (BRICK_WIDTH + BRICK_SPACING)
            y = BRICK_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING)
            if x + BRICK_WIDTH <= screen_width:
                bricks.append(
                    Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, COLORS['red'])  # 全用紅色方便辨識
                )
        return bricks

    @staticmethod
    def layout_default(screen_width, layout_offset_x):
        bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = layout_offset_x + col * (BRICK_WIDTH + BRICK_SPACING)
                y = BRICK_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING)

                if x + BRICK_WIDTH > screen_width:
                    continue

                bricks.append(
                    Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, Layouts.get_color_by_row(row))
                )
        return bricks

    @staticmethod
    def layout_zigzag(screen_width, layout_offset_x):
        bricks = []
        for row in range(BRICK_ROWS):
            offset = BRICK_WIDTH // 2 if row % 2 == 1 else 0

            for col in range(BRICK_COLS):
                x = layout_offset_x + offset + col * (BRICK_WIDTH + BRICK_SPACING)
                y = BRICK_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING)

                if (x + BRICK_WIDTH > screen_width or
                        y + BRICK_HEIGHT > screen_width * 0.8):
                    continue

                bricks.append(
                    Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, Layouts.get_color_by_row(row))
                )
        return bricks