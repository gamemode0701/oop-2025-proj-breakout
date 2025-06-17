from constants import COLORS, BRICK_ROWS, BRICK_COLS, BRICK_WIDTH, BRICK_HEIGHT, BRICK_SPACING, BRICK_OFFSET
from game_objects import Brick


class Layouts:
    @staticmethod
    def get_color_by_row(row):
        if row < 2:
            return COLORS['red']
        elif row < 4:
            return COLORS['orange']
        elif row < 6:
            return COLORS['yellow']
        elif row < 8:
            return COLORS['green']
        else:
            return COLORS['blue']

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
    def layout_cross(screen_width, layout_offset_x):
        bricks = []
        mid_row = BRICK_ROWS // 2
        mid_col = BRICK_COLS // 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                if row == mid_row or col == mid_col:
                    x = layout_offset_x + col * (BRICK_WIDTH + BRICK_SPACING)
                    y = BRICK_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING)

                    if x + BRICK_WIDTH <= screen_width:
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