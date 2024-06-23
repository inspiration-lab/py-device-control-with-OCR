import time

import pyautogui

# 不同分辨率下的坐标
resolution_group = {
    (3840, 2160): {
        # 待采集列表页
        "列表页初始坐标和间隔": (591, 243, 39),
        # 界面点选项
        "日": (338, 173),
        "数据导出": (678, 171),
        "关闭数据浏览页": (665, 128),
        # 应用内对话框项
        "全部数据": (1706, 935),
        "时间周期下拉列表": (1707, 1053),
        "时间周期下拉列表_日选项": (1691, 1242),
        "时间周期下拉列表_1分钟选项": (1670, 1079),
        "导出": (2003, 1269),
    }
}


def get_point(point_name):
    # 获取当前分辨率
    scr_size = pyautogui.size()

    if scr_size in resolution_group:
        # 获取坐标
        resolution = resolution_group[scr_size]
        if point_name in resolution:
            # print(f"Point for resolution {scr_size} is {resolution[point_name]}")
            return resolution[point_name]
        else:
            print("Point key not found in the coordinate map.")
            return None
    else:
        print(f"No coordinate map found for resolution {scr_size}.")
        return None


if __name__ == "__main__":
    time.sleep(2)
    print(*get_point("列表页初始坐标和间隔"))
    x, y, interval = get_point("列表页初始坐标和间隔")
    print(x, y, interval)
    # pyautogui.moveTo(*get_point("日"), duration=0.0)
