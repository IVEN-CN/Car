# 寻迹小车的颜色识别模块
# 此代码将在树莓派上运行

# 采用一个LED来指示代码运行的程度，用serial串口通信与单片机连接

# 使用方法
在运行main之前应该先用color_init初始化颜色阈值和识别面积，main识别的颜色会在阈值内，
并且面积应该大于等于预先调整的面积值。

# color_init
OpenCV没有内置的按钮，使用trackbar来充当按钮，0表示不保存，1表示保存，调整好一个颜色的阈值时先将color滑块
滑到对应的颜色，0表示红，1表示绿，2表示蓝，然后再滑动下方的save滑块到1，完成保存操作
