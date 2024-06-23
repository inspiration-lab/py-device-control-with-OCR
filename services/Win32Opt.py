import time

import pyautogui
import win32gui

from func.ResolutionGroup import get_point


def find_window_hwnd(title):
    """查找并返回指定标题的窗口句柄"""

    def enum_callback(hwnd, lparam):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd).startswith(title):
            # 收集句柄
            lparam.append(hwnd)

    hwnd_list = []
    win32gui.EnumWindows(enum_callback, hwnd_list)

    # 返回结果
    return hwnd_list if hwnd_list else None


def find_button_info(dialog_title, button_caption):
    """查找指定标题的对话框中特定名称的按钮，并返回其坐标及尺寸"""

    # 回调函数，添hwnd加到列表中
    def enum_window_proc(hwnd, lParam):
        lParam.append(hwnd)
        return True  # 继续枚举

    # 查找对话框
    dialog_hwnd = win32gui.FindWindow(None, dialog_title)
    if dialog_hwnd == 0:
        # print(f"未找到对话框'{dialog_title}'")
        return None
    else:
        # 聚焦对话框，提高命中几率
        win32gui.SetForegroundWindow(dialog_hwnd)

    # 获取对话框子集
    all_windows = []
    win32gui.EnumChildWindows(dialog_hwnd, enum_window_proc, all_windows)
    # 遍历子集，找出需要的元素
    for hwnd in all_windows:
        window_class = win32gui.GetClassName(hwnd)
        if window_class.lower() == "button":
            button_text = win32gui.GetWindowText(hwnd)
            if button_text == button_caption:  # 确保按钮文本匹配
                # 获取按钮的屏幕坐标及尺寸
                rect = win32gui.GetWindowRect(hwnd)
                x, y, right, bottom = rect
                width = right - x
                height = bottom - y
                return (x, y, width, height)  # 返回坐标及尺寸元组

    # print(f"未找到按钮'{button_caption}'")
    return None


def mouse_movement_path(type: str):
    # 等待稳定
    time.sleep(1)
    if type == "day":
        # 进入页面，移动选择【日】
        pyautogui.moveTo(*get_point("日"), duration=0.0)
        pyautogui.click()
        # 等待刷新
        time.sleep(1)
    # 平移到【数据导出】
    pyautogui.moveTo(*get_point("数据导出"), duration=0.0)
    pyautogui.click()
    time.sleep(0.5)
    # 点击单选按钮，确认【全部数据】
    # pyautogui.moveTo(*get_point("全部数据"), duration=0.0)
    # pyautogui.click()
    # 点击下拉菜单，选择【时间周期下拉列表】
    pyautogui.moveTo(*get_point("时间周期下拉列表"), duration=0.0)
    pyautogui.click()
    time.sleep(0.5)
    if type == "day":
        # 选择时间周期【日】
        pyautogui.moveTo(*get_point("时间周期下拉列表_日选项"), duration=0.0)
        pyautogui.click()
    if type == "min":
        # 选择时间周期【1分钟】
        pyautogui.moveTo(*get_point("时间周期下拉列表_1分钟选项"), duration=0.0)
        pyautogui.click()
    time.sleep(0.5)
    # 点击【导出】
    pyautogui.moveTo(*get_point("导出"), duration=0.0)
    time.sleep(0.5)
    pyautogui.click()
    # 移开鼠标。或手动改变另存为对话框初始位置，避免鼠标移动穿过对话框，引起误操作。可拖动改变初始位置，之后就每次出现在新位置
    pyautogui.moveTo(10, 10, duration=0.0)
    # 循环等对话框出现，循环获取坐标
    while True:
        time.sleep(0.5)
        button_info = find_button_info("另存为", "保存(&S)")
        if button_info:
            # 解包元组到单独的变量
            x, y, width, height = button_info
            # 使用这些值进行操作
            # print(f"按钮坐标：({x}, {y})")
            # print(f"按钮尺寸：{width}x{height}")
            pyautogui.moveTo(x + width / 2, y + height / 2, duration=0.0)
            time.sleep(1)
            pyautogui.click()
            # 此时对话框应不存在
            if find_window_hwnd("另存为") is None:
                break
    # 预览窗口出现标志，默认未出现；防止加载延迟
    preview_window_flag = False
    while True:
        time.sleep(1)
        # 检查坐标(100, 100)的像素颜色
        pixel_color = pyautogui.pixel(3297, 27)
        # 预览的excel标题栏颜色会随系统主题变化，应用窗口颜色不受影响，判断应用窗口是否消失相对准确
        if pixel_color != (48, 51, 54):
            # 点击关闭预览的excel文件
            pyautogui.moveTo(3838, 1, duration=0.0)
            time.sleep(1)
            pyautogui.click()
            time.sleep(0.2)
            # 更新状态，预览窗口已出现过
            preview_window_flag = True
        # 出现过，且完全关闭预览窗口才中止步骤
        if pixel_color == (48, 51, 54) and preview_window_flag:
            break
    # 点击关闭当前数据预览页，返回列表菜单
    pyautogui.moveTo(*get_point("关闭数据浏览页"), duration=0.0)
    time.sleep(0.5)
    pyautogui.click()


if __name__ == "__main__":
    DIALOG_TITLE = "另存为"
    BUTTON_TEXT = "取消"

    # 按钮名称: '保存(&S)'
    # 按钮名称: '取消'
    # 按钮名称: '帮助(&H)'

    print(find_window_hwnd(DIALOG_TITLE))
