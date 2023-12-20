import smbus
import time

# MPU6050寄存器
PWR_MGMT_1   = 0x6B  # 电源管理寄存器
SMPLRT_DIV   = 0x19  # 采样率分频寄存器
CONFIG       = 0x1A  # 配置寄存器
GYRO_CONFIG  = 0x1B  # 陀螺仪配置寄存器
INT_ENABLE   = 0x38  # 中断使能寄存器
ACCEL_XOUT_H = 0x3B  # 加速度计X轴高位寄存器
ACCEL_YOUT_H = 0x3D  # 加速度计Y轴高位寄存器
ACCEL_ZOUT_H = 0x3F  # 加速度计Z轴高位寄存器
GYRO_XOUT_H  = 0x43  # 陀螺仪X轴高位寄存器
GYRO_YOUT_H  = 0x45  # 陀螺仪Y轴高位寄存器
GYRO_ZOUT_H  = 0x47  # 陀螺仪Z轴高位寄存器

def MPU_Init():
    # 写入采样率分频寄存器
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    # 写入电源管理寄存器
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    # 写入配置寄存器
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    # 写入陀螺仪配置寄存器
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    # 写入中断使能寄存器
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    # 加速度计和陀螺仪的值是16位的
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    # 将高位和低位值拼接起来
    value = ((high << 8) | low)
    
    # 获取mpu6050的有符号值
    if(value > 32768):
        value = value - 65536
    return value

if __name__ == '__main__':
    bus = smbus.SMBus(1)  # 或者bus = smbus.SMBus(0)适用于旧版本的板子
    Device_Address = 0x68   # MPU6050设备地址

    MPU_Init()

    while True:
        
        # 读取加速度计数据
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        
        # 读取陀螺仪数据
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
        
        # 打印数据
        print("陀螺仪X轴:", gyro_x, "陀螺仪Y轴:", gyro_y, "陀螺仪Z轴:", gyro_z)
        print("加速度计X轴:", acc_x, "加速度计Y轴:", acc_y, "加速度计Z轴:", acc_z)
        
        # 延时
        time.sleep(1)