import pyautogui
import pytesseract
from PIL import Image

if __name__ == '__main__':
    # 设置pytesseract的tesseract命令路径
    pytesseract.pytesseract.tesseract_cmd = r"C:\custom\Tesseract-OCR\tesseract.exe"

    # 截取图像
    screenshot = pyautogui.screenshot(region=(1341, 1158, 669, 108))
    # 显示图像
    screenshot.show()
    # 将图像转换为Pillow图像对象
    img = Image.frombytes("RGB", (669, 108), screenshot.tobytes())
    # 使用pytesseract进行OCR识别
    result = pytesseract.image_to_string(img, lang="chi_sim")

    print(result)
