import win32con
import win32gui


def find_and_activate_window(window_name):
    """根据窗口标题查找窗口并激活"""
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd != 0:
        win32gui.SetForegroundWindow(hwnd)
        print(f"窗口'{window_name}'已被激活")
    else:
        print(f"未找到窗口'{window_name}'")


def send_message_to_window(window_name, message_id, message_wparam=0, message_lparam=0):
    """向指定窗口发送消息"""
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd != 0:
        win32gui.SendMessage(hwnd, message_id, message_wparam, message_lparam)
        print(f"消息已发送到窗口'{window_name}'")
    else:
        print(f"未找到窗口'{window_name}'")


def find_window_hwnd(title):
    """查找并返回指定标题的窗口句柄"""

    def enum_callback(hwnd, lparam):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd).startswith(title):
            # 回调不能返回True或False
            lparam.append(hwnd)  # 收集句柄而非关闭窗口
        #     return False  # 结束枚举
        # return True

    hwnd_list = []  # 使用列表来收集句柄
    win32gui.EnumWindows(enum_callback, hwnd_list)

    # 返回结果
    return hwnd_list if hwnd_list else None


def click_button(hwnd_parent, class_name, button_text):
    """在指定父窗口下查找并点击按钮"""
    button_hwnd = win32gui.FindWindowEx(hwnd_parent, None, class_name, button_text)
    if button_hwnd:
        # 无效，不会触发事件
        win32gui.PostMessage(button_hwnd, win32con.BN_CLICKED, 0, 0)
        print(f"按钮'{button_text}'已点击")
    else:
        print(f"未找到按钮'{button_text}'")


def enum_child_windows(hwnd, results):
    """递归遍历子窗口的函数"""
    child = win32gui.FindWindowEx(hwnd, None, None, None)
    while child:
        results.append(child)
        # 继续枚举子窗口
        enum_child_windows(child, results)
        child = win32gui.FindWindowEx(hwnd, child, None, None)


def find_and_print_buttons_with_position(dialog_title):
    """查找指定标题的对话框，并打印其中所有按钮的名称及其坐标"""
    # 查找对话框
    dialog_hwnd = win32gui.FindWindow(None, dialog_title)
    if dialog_hwnd == 0:
        print(f"未找到对话框'{dialog_title}'")
        return

    # 遍历对话框及其子窗口
    all_windows = []
    enum_child_windows(dialog_hwnd, all_windows)

    # 检查并打印按钮名称及其坐标
    for hwnd in all_windows:
        window_class = win32gui.GetClassName(hwnd)
        if window_class.lower() == "button":
            button_text = win32gui.GetWindowText(hwnd)
            if button_text:  # 确保按钮有文本才打印
                # 获取按钮的屏幕坐标
                rect = win32gui.GetWindowRect(hwnd)
                x, y, right, bottom = rect
                width = right - x
                height = bottom - y
                print(f"按钮名称: '{button_text}', 左上角坐标: ({x}, {y}), 尺寸: ({width}x{height})")

if __name__ == "__main__":
    find_and_activate_window("窗口标题")