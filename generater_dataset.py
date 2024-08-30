import numpy as np
import win32gui, win32ui, win32con
from PIL import Image
from time import sleep
import os

class WindowCapture:
    w = 1400  # Укажи нужную ширину окна
    h = 800  # Укажи нужную высоту окна
    hwnd = None

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # Теперь размеры окна задаются вручную
        self.cropped_x = 0  # Укажи смещение по X (граница окна)
        self.cropped_y = 0  # Укажи смещение по Y (заголовок окна)

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]  # Убираем альфа-канал
        img = np.ascontiguousarray(img)
        
        return img
        
    def generate_image_dataset(self):
        """Generate a dataset of screenshots."""
        if not os.path.exists("images"):
            os.mkdir("images")
        while True:
            img = self.get_screenshot()
            im = Image.fromarray(img[..., [2, 1, 0]])  # Convert BGR to RGB
            im.save(f"./images/img_{len(os.listdir('images'))}.jpg")
            sleep(0.3)
            
window_name = "Minecraft* 1.19.2 - Одиночная игра"

wincap = WindowCapture(window_name)
wincap.generate_image_dataset()