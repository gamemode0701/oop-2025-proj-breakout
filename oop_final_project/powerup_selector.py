import random
from campy.graphics.gobjects import GLabel, GRect
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause

def choose_from_two_powerups(window):
    """
    隨機顯示兩個道具選項，等待玩家點擊選擇，回傳選到的道具種類
    """
    all_options = ['add_ball', 'multi_ball', 'slow', 'bomb', 'wide_paddle']  # 所有道具種類

    # 展示用的對應顯示文字（含換行）
    display_map = {
        'add_ball': 'ADD\nBALL',
        'multi_ball': 'MULTI\nBALL',
        'slow': 'SLOW',
        'bomb': 'BOMB',
        'wide_paddle': 'WIDE\nPADDLE'
    }

    options = random.sample(all_options, 2)  # 隨機選兩個
    buttons = []  # 存放按鈕(GRect)物件
    selected = {'choice': None}  # 用 dict 包裝，方便在內部函式修改

    # 根據視窗大小動態設定按鈕尺寸
    btn_width = window.width * 0.3
    btn_height = window.height * 0.6
    gap = 15  # 兩按鈕間隔
    boarder = 10  # 黃色背板比按鈕大10單位

    # 計算兩個按鈕的總寬度，讓它們水平置中
    total_width = btn_width * 2 + gap
    start_x = (window.width - total_width) / 2
    y = (window.height - btn_height) / 2  # 讓按鈕垂直置中

    for i, opt in enumerate(options):
        # 黃色背板
        board_rect = GRect(btn_width + boarder, btn_height + boarder)
        board_rect.filled = True
        board_rect.fill_color = '#FFD600'  # 深一點的黃色
        board_rect.color = '#FFD600'
        x = start_x + i * (btn_width + gap) - boarder / 2
        window.add(board_rect, x, y - boarder / 2)

        # 綠色按鈕
        rect = GRect(btn_width, btn_height)
        rect.filled = True
        rect.fill_color = '#90ee90'  # 淺綠色
        rect.color = '#90ee90'  # 不要黑框
        btn_x = start_x + i * (btn_width + gap)
        window.add(rect, btn_x, y)

        # 按鈕文字（支援換行）
        display_text = display_map[opt]
        lines = display_text.split('\n')
        total_label_height = 0
        labels = []
        # 先計算總高度
        for line in lines:
            label = GLabel(line)
            label.font = 'Consolas-20'
            total_label_height += label.height
            labels.append(label)
        # 計算第一行的 y 座標，讓多行置中
        current_y = y + (btn_height - total_label_height) / 2
        for label in labels:
            label_x = btn_x + (btn_width - label.width) / 2
            label_y = current_y + label.height
            window.add(label, label_x, label_y)
            current_y += label.height

        # 綁定資料
        rect.option = opt
        rect.base_color = '#90ee90'
        rect.hover_color = 'cyan'
        rect.labels = labels  # 多行label
        rect.x0 = btn_x
        rect.y0 = y
        rect.width0 = btn_width
        rect.height0 = btn_height
        buttons.append(rect)

    # 滑鼠點擊事件
    def handle_click(event):
        for btn in buttons:
            if btn.x0 <= event.x <= btn.x0 + btn.width0 and btn.y0 <= event.y <= btn.y0 + btn.height0:
                selected['choice'] = btn.option

    # 滑鼠移動事件（hover效果）
    def handle_hover(event):
        for btn in buttons:
            if btn.x0 <= event.x <= btn.x0 + btn.width0 and btn.y0 <= event.y <= btn.y0 + btn.height0:
                btn.fill_color = btn.hover_color
            else:
                btn.fill_color = btn.base_color

    onmouseclicked(handle_click)
    onmousemoved(handle_hover)

    # 等待玩家選擇
    while selected['choice'] is None:
        pause(100)

    # 移除所有按鈕和標籤
    for btn in buttons:
        window.remove(btn)
        for label in btn.labels:
            window.remove(label)

    # 也要移除黃色背板
    for i in range(2):
        x = start_x + i * (btn_width + gap) - boarder / 2
        board_rect = window.get_object_at(x + 1, y + 1)
        if board_rect:
            window.remove(board_rect)

    return selected['choice']  # 回傳玩家選到的道具
