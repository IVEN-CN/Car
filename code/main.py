"""
执行过程的主文件
黄色灯亮 -> 识别二维码 -> 识别完成 -> 发送信号1 -> 黄色灯灭 -> 颜色识别 -> 识别完成 -> 发生信号2 ->黄色灯
"""
import time
import cv2
import serial
import numpy as np
import threading
import RPi.GPIO as IO


def detectQR(cap_) -> str:
    """识别二维码"""
    while cap_.isOpened():
        ret, frm = cap_.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            det = cv2.QRCodeDetector()
            codeinfo, points, straight_qrcode = det.detectAndDecode(_img)
            if codeinfo != '':
                return codeinfo


def detectCOLOR(cap_, lowrange, uprange, area):
    """颜色识别函数"""

    while cap_.isOpened():
        ret, frm = cap_.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(_img, lowrange, uprange)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if not ret:
                break
            else:
                for contour in contours:
                    # 对每个轮廓进行矩形拟合
                    x, y, w, h = cv2.boundingRect(contour)
                    brcnt = np.array([[[x, y]], [[x + w, y]], [[x + w, y + h]], [[x, y + h]]])
                    if w * h >= area:
                        cv2.drawContours(frm, [brcnt], -1, (255, 255, 255), 2)

                        return w * h


def readfile(sign) -> np.ndarray:
    """通过识别的二维码选择对应的颜色"""
    global filename
    if sign[:2] == '11':
        filename = 'Red.npy'
    if sign[:2] == '22':
        filename = 'Green.npy'
    if sign[:2] == '33':
        filename = 'Blue.npy'

    arr = np.load(filename)
    return arr


def read_area():
    return np.load('area.npy')


class LED:
    def __init__(self, point):
        """point是针脚对应的BCM编码"""
        self.point = point
        IO.setmode(IO.BCM)
        IO.setup(self.point, IO.OUT)
        # self.ld = IO.PWM(self.point, 500)
        # self.ld.start(0)

    def led_on(self):
        IO.setup(self.point, IO.OUT)
        IO.output(self.point, IO.HIGH)

    def led_off(self):
        IO.setup(self.point, IO.OUT)
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

    # 创建蓝色LED对象,BCM 18号引脚是GPIO.1，用于指示二维码的识别
    Led = LED(18)


    def main():
        # region 二维码识别
        # 打开蓝色LED
        Led.led_on()

        # 识别二维码
        info = detectQR(cap)
        # 发送串口信号：1
        ser.write(b'1')

        # 关闭二维码指示LED
        Led.led_off()
        # endregion

        # region 颜色识别
        # 读取颜色信息
        threshold = readfile(info)

        area = read_area()

        # 识别颜色
        detectCOLOR(cap, threshold[0], threshold[1], area)

        # 发送串口信号：2
        ser.write(b'2')

        # 添加闪烁进程
        threading.Thread(Led.blink()).start()
        # endregion

    # 创建主线程
    threading.Thread(target=main).start()
