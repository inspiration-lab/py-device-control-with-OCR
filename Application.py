import re
import time

import pyautogui
import pytesseract
from PIL import Image
from sqlalchemy import text

from func.ResolutionGroup import get_point
from services.DatabaseOpt import DatabaseOpt
from services.Win32Opt import mouse_movement_path

# 设置pytesseract的tesseract命令路径
pytesseract.pytesseract.tesseract_cmd = r"C:\custom\Tesseract-OCR\tesseract.exe"


def run():
    # 引入数据库操作实例
    db = DatabaseOpt()
    # 匹配独立的8位数字序列
    pattern = r"\b\d{8}\b"

    for page in range(1, 42):
        # 截取图像
        screenshot = pyautogui.screenshot(region=(490, 220, 160, 1770))
        # 显示图像
        # screenshot.show()
        # 将图像转换为Pillow图像对象
        img = Image.frombytes("RGB", (160, 1770), screenshot.tobytes())
        # 使用pytesseract进行OCR识别
        result = pytesseract.image_to_string(img, lang="eng")

        # 执行匹配
        matches_list = re.findall(pattern, result)
        # 遍历匹配结果
        for index, code in enumerate(matches_list):
            # 构建查询语句
            result = db.execute_sql("primary_db", text(f"select id from processed_codes where code = '{code}'"))
            # 检查查询结果，不为None或空执行
            if not result:
                # 移动鼠标到第index项
                x, y, interval = get_point("列表页初始坐标和间隔")
                pyautogui.moveTo(x, y + interval * index, duration=0.0)
                pyautogui.doubleClick()
                # 开始进行页面内操作
                mouse_movement_path("day")
                mouse_movement_path("min")
                # 已处理，添加编号到数据库
                db.execute_sql("primary_db", text(
                    f"insert into processed_codes (code, create_time) values ('{code}', now() at time zone 'PRC');"))
            else:
                print(f"Code={{{code}}} already exists in the database.")
        # 翻页
        print(f"完成 Page: {page}")
        time.sleep(1)
        pyautogui.press("pagedown")
        time.sleep(1)


if __name__ == "__main__":
    # 等待后执行
    time.sleep(3)
    run()
