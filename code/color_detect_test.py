"""使用HSV色彩范围进行颜色识别"""

import cv2
import numpy as np


def callback(x):
    return x


roll = np.ones((7, 7), np.uint8)
# 获取摄像头信息
cap = cv2.VideoCapture(1)

# def color_detect(frm):
#     """返回二值图"""
cv2.namedWindow('color_detect')
L_H = 0
H_H = 180
L_S = 0
H_S = 255
L_V = 0
H_V = 255
cv2.createTrackbar('lower_H', 'color_detect', L_H, 180, callback)
cv2.createTrackbar('upper_H', 'color_detect', H_H, 180, callback)
cv2.createTrackbar('lower_S', 'color_detect', L_S, 255, callback)
cv2.createTrackbar('upper_S', 'color_detect', H_S, 255, callback)
cv2.createTrackbar('lower_V', 'color_detect', L_V, 255, callback)
cv2.createTrackbar('upper_V', 'color_detect', H_V, 255, callback)

while cap.isOpened():
    # read返回两个值，ret是是否读取成功的bool值，frm是每帧的数据
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    L_H = cv2.getTrackbarPos('lower_H', 'color_detect')
    H_H = cv2.getTrackbarPos('upper_H', 'color_detect')
    L_S = cv2.getTrackbarPos('lower_S', 'color_detect')
    H_S = cv2.getTrackbarPos('upper_S', 'color_detect')
    L_V = cv2.getTrackbarPos('lower_V', 'color_detect')
    H_V = cv2.getTrackbarPos('upper_V', 'color_detect')

    low_color = np.array([L_H, L_S, L_V])
    up_color = np.array([H_H, H_S, H_V])
    mask = cv2.inRange(img, low_color, up_color)
    result = cv2.morphologyEx(mask,cv2.MORPH_OPEN,roll)
    if not ret:
        break
    else:
        # result = color_detect(frame)
        cv2.imshow('oring', frame)
        cv2.imshow('color_detect', mask)
        cv2.imshow('result',result)
        if cv2.waitKey(1) == 27:  # esc退出
            break

cap.release()
cv2.destroyAllWindows()
