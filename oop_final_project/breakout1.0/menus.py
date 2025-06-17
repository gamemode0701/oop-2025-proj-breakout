from campy.graphics.gobjects import GRect, GLabel
from campy.gui.events.timer import pause

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

def pause_menu(window):
    """暫停選單，讓玩家選擇繼續、重來或強制返回主選單"""
    from campy.gui.events.mouse import onmouseclicked, onmousemoved

    options = [
        {'text': 'continue', 'color': 'lightgreen', 'hover': 'green'},
        {'text': 'retry', 'color': 'yellow', 'hover': 'orange'},
        {'text': 'back to menu', 'color': 'red', 'hover': '#b22222'}
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
        for btn in buttons:
            if btn.x0 <= event.x <= btn.x0 + btn.width0 and btn.y0 <= event.y <= btn.y0 + btn.height0:
                choice['value'] = btn.option

    def hover_handler(event):
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
    if choice['value'] == 'continue':
        return 'continue'
    elif choice['value'] == 'retry':
        return 'retry'
    else:
        return 'menu'







