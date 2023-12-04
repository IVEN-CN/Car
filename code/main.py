"""执行过程的主文件
1.根据树莓派的串口设置串口名称和波特率
3.创建一个合适大小的卷积核"""

import cv2
import serial
import numpy as np

check_arr = np.ones()  # 需要输入卷积核尺寸


def detectQR() -> tuple:
    """识别二维码"""
    # 创建摄像头对象
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frm = cap.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            det = cv2.QRCodeDetector()
            codeinfo, points, straight_qrcode = det.detectAndDecode(_img)
            if codeinfo != '':
                return codeinfo, 1


def detectCOLOR(lowrange, uprange):
    """颜色识别函数"""
    # 创建摄像头对象
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frm = cap.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            mask = cv2.inRange(_img, lowrange, uprange)
            if np.isin(check_arr, mask):
                return mask, 2


def readfile(sign):
    if sign == '11':
        filename = 'Red'
    if sign == '22':
        filename = 'Green'
    if sign == '33':
        filename = 'Blue'

    arr = np.load(filename)
    return arr


if __name__ == '__main__':
    # 创建串口对象
    ser = serial.Serial()  # 需要完善串口名和波特率(9600)

    info, sign = detectQR()
    # 发送串口信号：1
    ser.write(sign)

    # 颜色识别
    threshold = readfile(info)
    img,sing_dump = detectCOLOR(threshold[0],threshold[1])
    # 发送串口信号：2
    ser.write(sing_dump)
