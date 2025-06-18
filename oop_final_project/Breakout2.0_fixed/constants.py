import pygame
import math

# 初始化
pygame.init()
pygame.font.init()

# 常數設定
SCREEN_WIDTH = 600
MIN_WIDTH = 600
MAX_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60
BRICK_ROWS = 10  # 減少行數確保不會太高
BRICK_COLS = 10  # 標準列數
BRICK_WIDTH = 40
BRICK_HEIGHT = 15
BRICK_SPACING = 5  # 間距不宜過大
BRICK_OFFSET = 50  # 頂部間距
PADDLE_WIDTH = 75
PADDLE_HEIGHT = 15
PADDLE_OFFSET = 50
BALL_RADIUS = 10
EXTRA_BALL_RADIUS = 6
INITIAL_Y_SPEED = 5
MAX_X_SPEED = 5
NUM_LIVES = 3
BOMB_RADIUS = 100

# 顏色定義
COLORS = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'cyan': (0, 255, 255),
    'crimson': (220, 20, 60),
    '#b22222': (178, 34, 34),
    'magenta': (255, 0, 255),
    'darkgreen': (0, 100, 0)
}

# 勝利動畫用顏色及偵數
WIN_ANIMATION = {
    'colors': ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'cyan', 'crimson'],
    'phase1_frames': 120,  # 第一階段幀數
    'phase2_frames': 30,  # 第二階段幀數
    'phase3_frames': 60,  # 第三階段幀數
}

# 磚頭顏色
BRICK_COLORS = {
    0: 'red',  # 第0-1行
    2: 'orange',  # 第2-3行
    4: 'yellow',  # 第4-5行
    6: 'green',  # 第6-7行
    8: 'blue',  # 第8-9行
}

# 技能道具的顏色和icon
POWERUPS = {
    'add_ball': {'color': 'green', 'icon': '1️⃣'},
    'multi_ball': {'color': 'orange', 'icon': '3️⃣'},
    'slow': {'color': 'blue', 'icon': '❄️'},
    'bomb': {'color': 'red', 'icon': '💣'},
    'wide_paddle': {'color': 'purple', 'icon': '↔️'},
    'penetrate': {'color': 'magenta', 'icon': '⚡️'},
}
