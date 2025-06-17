import random
from campy.graphics.gobjects import GRect, GLabel
from campy.gui.events.timer import pause
from campy.graphics.gwindow import GWindow
import os

def lost_animation(window):
    """遊戲失敗動畫：讀取 location.txt 畫出像素藝術，然後逐漸消失"""
    window.clear()
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'location.txt')
    coords = []
    x = None

    # 讀取像素座標
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # 跳過空行
                continue
            if line.startswith('x') and line[1:].isdigit():
                x = int(line[1:])
            elif line.startswith('y') and line[1:].isdigit() and x is not None:
                y = int(line[1:])
                coords.append((x, y))
                x = None  # 重設 x
            # 跳過像 'G1', 'A2' 這種標籤行

    # 計算圖形範圍
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)

    art_width = max_x - min_x
    art_height = max_y - min_y

    # 計算置中偏移量
    x_offset = (window.width - art_width) // 2 - min_x
    y_offset = (window.height - art_height) // 2 - min_y

    # 套用偏移量讓圖形置中
    coords = [(x + x_offset, y + y_offset) for x, y in coords]

    # 畫出像素藝術
    for x, y in coords:
        pixel = GRect(6, 6)
        pixel.filled = True
        pixel.fill_color = 'crimson'
        pixel.color = 'crimson'
        window.add(pixel, x=x, y=y)
        pause(1)  # 畫每個像素時稍作停頓

    pause(3000)  # 停留 3 秒

    # 淡出動畫：隨機移除像素
    fade_count = 0
    total_to_fade = len(coords)
    while fade_count < total_to_fade:
        i = random.randint(0, len(coords) - 1)
        x, y = coords[i]
        obj = window.get_object_at(x + 3, y + 3)
        if obj is not None:
            window.remove(obj)
            fade_count += 1
            pause(2)

def win_animation(window):
    """遊戲勝利動畫：顯示 YOU WIN! 並有彩色變化與灑花效果"""
    text = GLabel("YOU WIN!")
    text.font = "-40-bold"
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "cyan", "magenta"]
    window.add(text, x=(window.width - text.width) / 2, y=window.height / 2)
    # 文字顏色動畫
    for _ in range(30):  # 約 3 秒，每 0.1 秒換色
        text.color = random.choice(colors)
        pause(100)

    # 簡單灑花效果
    for _ in range(150):
        x = random.randint(0, window.width)
        y = random.randint(0, window.height)
        dot = GLabel("*")
        dot.font = "-20"
        dot.color = random.choice(colors)
        window.add(dot, x=x, y=y)
        pause(10)