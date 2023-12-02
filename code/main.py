"""执行过程的主文件
1.根据树莓派的串口设置串口名称和波特率
2.单片机没有传回的信号时是不是0？
3.创建一个合适大小的卷积核"""

import cv2
import serial
import numpy as np


def detectQR(_img) -> tuple:
    """识别二维码"""
    det = cv2.QRCodeDetector()
    try:
        codeinfo, points, straight_qrcode = det.detectAndDecode(_img)
        return codeinfo, 1
    except:
        return None, 0


def detectCOLOR(_img, lowrange, uprange):
    mask = cv2.inRange(_img, lowrange, uprange)
    return mask


# 创建摄像头对象
cap = cv2.VideoCapture(0)
# 创建串口对象
ser = serial.Serial()  # 需要完善串口名和波特率

while cap.isOpened():
    sign = 0
    ret, frame = cap.read()
    img_Gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 用于识别二维码的灰度图
    img_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 用于颜色识别的HSV色彩空间
    # 读取个字节的串口数据
    sign_QR = ser.read(1)

    if sign_QR == 1:
        """识别到黑线"""
        # 尝试识别二维码
        data_QR, sign = detectQR(img_Gray)
        # 传回信号
        ser.write(sign)
    else:
        pass
