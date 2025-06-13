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

def game_over_menu(window):
    """遊戲結束選單，讓玩家選擇重來、回主選單或離開（含按鈕底色與 hover 效果，字型 Consolas-20，按鈕置中）"""
    from campy.gui.events.mouse import onmouseclicked, onmousemoved

    options = [
        {'text': 'retry', 'color': 'yellow', 'hover': 'orange'},
        {'text': 'back to menu', 'color': 'yellow', 'hover': 'orange'},
        {'text': 'exit', 'color': 'red', 'hover': '#b22222'}
    ]
    choice = {'value': None}
    buttons = []

    btn_width = 220
    btn_height = 40
    btn_space = 30  # 按鈕間距

    # 計算三個按鈕的總高度，讓它們垂直置中
    total_height = 3 * btn_height + 2 * btn_space
    start_y = (window.height - total_height) // 2

    for i, opt in enumerate(options):
        # 建立按鈕底色
        rect = GRect(btn_width, btn_height)
        rect.filled = True
        rect.fill_color = opt['color']
        rect.color = 'black'
        x = (window.width - btn_width) / 2
        y = start_y + i * (btn_height + btn_space)
        window.add(rect, x, y)
        # 建立文字
        label = GLabel(opt['text'])
        label.font = 'Consolas-20'
        label_x = x + (btn_width - label.width) / 2
        label_y = y + btn_height * 0.85
        window.add(label, label_x, label_y)
        # 綁定資料
        rect.option = opt['text']
        rect.base_color = opt['color']
        rect.hover_color = opt['hover']
        rect.label = label
        rect.x0 = x
        rect.y0 = y
        rect.width0 = btn_width
        rect.height0 = btn_height
        buttons.append(rect)

    def click_handler(event):
        # 檢查滑鼠是否點擊到按鈕
        for btn in buttons:
            if btn.x0 <= event.x <= btn.x0 + btn.width0 and btn.y0 <= event.y <= btn.y0 + btn.height0:
                choice['value'] = btn.option

    def hover_handler(event):
        # 滑鼠移到按鈕上時變色，離開時恢復
        for btn in buttons:
            if btn.x0 <= event.x <= btn.x0 + btn.width0 and btn.y0 <= event.y <= btn.y0 + btn.height0:
                btn.fill_color = btn.hover_color
            else:
                btn.fill_color = btn.base_color

    onmouseclicked(click_handler)
    onmousemoved(hover_handler)

    # 等待玩家選擇
    while choice['value'] is None:
        pause(100)

    # 移除所有按鈕和標籤
    for btn in buttons:
        window.remove(btn)
        window.remove(btn.label)

    # 回傳對應選項
    if choice['value'] == 'retry':
        return 'retry'
    elif choice['value'] == 'back to menu':
        return 'menu'
    else:
        return 'exit'


