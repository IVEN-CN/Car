"""
执行过程的主文件
创建一个合适大小的卷积核（用于颜色识别）
"""
import time
import cv2
import serial
import numpy as np
import threading
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


def detectCOLOR(cap_, lowrange, uprange) -> int:
    """颜色识别函数"""
    # 创建摄像头对象

    while cap_.isOpened():
        ret, frm = cap_.read()
        if ret:
            _img = cv2.cvtColor(frm, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(_img, lowrange, uprange)
            if np.isin(check_arr, mask):
                return 2


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
        IO.setup(18,IO.OUT)
        self.ld = IO.PWM(self.point, 500)
        self.ld.start(0)

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

    def __breath_up(self):
        for i in range(101):
            self.ld.ChangeDutyCycle(i)
            time.sleep(0.05)

    def __breath_down(self):
        for i in range(100, 0, -1):
            self.ld.ChangeDutyCycle(i)
            time.sleep(0.05)

    def breath(self):
        while 1:
            self.__breath_up()
            self.__breath_down()


if __name__ == '__main__':
    # 创建摄像头对象
    cap = cv2.VideoCapture(0)

    # 创建串口对象
    ser = serial.Serial('/dev/ttyAMA0', 9600)

    # 创建蓝色LED对象,BCM 18号引脚是GPIO.1，用于指示二维码的识别
    LED_blue = LED(18)

    # 创建绿色LED,BCM 12号对应GPIO.27,用于指示颜色识别
    LED_green = LED(12)

    # 创建呼吸灯对象，BCM 5号（GPIO.21)接正极，6号接负极,用于指示程序运行
    LED_breath = LED(5)

    # 创建闪烁LED,BCM 26号对应GPIO.25,用于指示算法结束
    LED_blink = LED(26)

    def main():

        # region 二维码识别
        # 打开蓝色LED
        LED_blue.led_on()

        # 识别二维码
        info = detectQR(cap)
        # 发送串口信号：1
        ser.write(b'1')

        # 关闭二维码指示LED
        LED_blue.led_off()
        # 添加闪烁进程
        threading.Thread(LED_blink.blink()).start()
        # endregion

        # region 颜色识别
        # 读取颜色信息
        threshold = readfile(info)

        # 打开指示灯
        LED_green.led_on()

        # 识别颜色
        detectCOLOR(cap, threshold[0], threshold[1])

        # 发送串口信号：2
        ser.write(b'2')

        # 关闭指示灯
        LED_green.led_off()
        # 添加闪烁进程
        threading.Thread(LED_blink.blink()).start()
        # endregion

    def breath():
        LED_breath.breath()

    # 创建主线程
    threading.Thread(target=main).start()
    # 创建子线程
    threading.Thread(target=breath,daemon=True).start()