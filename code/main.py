"""
执行过程的主文件
1.根据树莓派的串口设置串口名称和波特率（建立串口通信）
3.创建一个合适大小的卷积核（用于颜色识别）
4.如何让LED闪烁
5.建立多线程，颜色识别和二维码识别的时候都要闪烁LED同时不影响画面流程，每个过程完成之后LED的颜色或者频率应该发生变化
"""

import cv2
import serial
import numpy as np
import RPi.GPIO as IO

check_arr = np.ones()  # 需要输入卷积核尺寸


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


def detectCOLOR(cap_, lowrange, uprange) -> str:
    """颜色识别函数"""
    # 创建摄像头对象

    while cap_.isOpened():
        ret, frm = cap_.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            mask = cv2.inRange(_img, lowrange, uprange)
            if np.isin(check_arr, mask):
                return mask


def readfile(sign) -> np.ndarray:
    """通过识别的二维码选择对应的颜色"""
    if sign == '11':
        filename = 'Red'
    if sign == '22':
        filename = 'Green'
    if sign == '33':
        filename = 'Blue'

    arr = np.load(filename)
    return arr


class LED:
    def __init__(self, point):
        """point是针脚对应的BCM编码"""
        self.point = point
        IO.setmode(IO.BCM)

    def led_on(self):
        IO.setup(self.point, IO.OUT)
        IO.output(self.point, IO.HIGH)

    def led_off(self):
        IO.setup(self.point, IO.OUT)
        IO.output(self.point, IO.LOW)


if __name__ == '__main__':
    # 创建摄像头对象
    cap = cv2.VideoCapture(0)

    # 创建串口对象
    ser = serial.Serial('/dev/ttyAMA0', 9600)

    info = detectQR(cap)
    # 发送串口信号：1
    ser.write(b'1')

    # 颜色识别
    threshold = readfile(info)
    img = detectCOLOR(cap, threshold[0], threshold[1])
    # 发送串口信号：2
    ser.write(b'2')
