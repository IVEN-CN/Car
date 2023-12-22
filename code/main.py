"""
执行过程的主文件
1.黄色灯亮起，可能表示系统开始工作。
2.系统开始识别二维码。
3.二维码识别完成。
4.黄色灯灭，可能表示二维码识别的阶段已经结束。
5.开始颜色识别。
6.颜色识别完成。
7.发送信号1，可能是通知电控系统，颜色识别已完成。
8.黄色灯闪烁，可能表示整个过程结束。
"""
import time
import cv2
import serial
import numpy as np
import threading
import RPi.GPIO as IO


def detectQR(cap_:cv2.Mat) -> str:
    """识别二维码"""
    while cap_.isOpened():
        ret, frm = cap_.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            det = cv2.QRCodeDetector()
            codeinfo, points, straight_qrcode = det.detectAndDecode(_img)
            if codeinfo != '':
                return codeinfo


def detectCOLOR(cap_:cv2.Mat, 
                lowrange:np.ndarray,
                uprange:np.ndarray, 
                area:np.ndarray) -> bool:
    """颜色识别函数"""

    while cap_.isOpened():
        ret, frm = cap_.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(_img, lowrange, uprange)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if not ret:
                return False
            for contour in contours:
                # 对每个轮廓进行矩形拟合
                x, y, w, h = cv2.boundingRect(contour)
                brcnt = np.array([[[x, y]], [[x + w, y]], [[x + w, y + h]], [[x, y + h]]])
                if w * h >= area:
                    cv2.drawContours(frm, [brcnt], -1, (255, 255, 255), 2)
                    return True


def readfile(sign) -> np.ndarray:
    """通过识别的二维码选择对应的颜色"""
    filename = {
        '11': 'Red.npy',
        '22': 'Green.npy',
        '33': 'Blue.npy'
    }
    arr = np.load(filename.get(sign[:2], ''))
    return arr


def read_area() -> np.ndarray:
    return np.load('area.npy')


class LED:
    def __init__(self, point):
        """point是针脚对应的BCM编码"""
        self.point = point
        IO.setmode(IO.BCM)
        IO.setup(self.point, IO.OUT)

    def led_on(self):
        IO.output(self.point, IO.HIGH)

    def led_off(self):
        IO.output(self.point, IO.LOW)

    def blink(self):
        self.led_on()
        time.sleep(0.25)
        self.led_off()
        time.sleep(0.25)


if __name__ == '__main__':
    # region 创建对象
    # 创建摄像头对象
    cap = cv2.VideoCapture(0)

    # 创建串口对象
    ser = serial.Serial('/dev/ttyAMA0', 9600)

    # 创建黄色LED对象,BCM 18号引脚是GPIO.1，用于指示二维码的识别
    Led = LED(18)
    # endregion


    def main():
        # region 二维码识别
        # 打开LED
        Led.led_on()

        # 识别二维码
        info = detectQR(cap)

        # 关闭二维码指示LED
        Led.led_off()
        # endregion

        # region 颜色识别
        # 读取颜色信息
        threshold = readfile(info)

        area = read_area()

        # 识别颜色
        detectCOLOR(cap, threshold[0], threshold[1], area)

        # 发送串口信号：1
        ser.write(b'1')

        # 添加闪烁进程
        threading.Thread(Led.blink()).start()
        # endregion

    # 创建主线程
    threading.Thread(target=main).start()
