"""将颜色识别信息储存到文件"""
import cv2

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # ret是读取标记，img是读取内容
    ret, img0 = cap.read()

    # 转换色彩空间
    img1 = cv2.cvtColor(img0, cv2.COLOR_BGR2HSV)

    # 展示窗口
    cv2.imshow('test', img1)

    # esc退出
    if cv2.waitKey(1) == 27:
        break

# 摧毁窗口
cv2.destroyAllWindows()

# 释放摄像头
cap.release()
