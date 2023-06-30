# 导入GPIO控制薄块
import RPi.GPIO as GPIO

# 导入time模块
import time

# 设置使用的引脚编码模式
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# 定义开关引脚
swi = 31
# 进行开关引脚的初始化，设置为输入引脚，且默认为高电平

GPIO.setup(swi, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 定义状态变化的回调函数
def switch(channel):
    # 高电平的开关松开
    if GPIO.input(channel):
        print("release")
        # 低电平为开关按下
    else:
        print("pressed")

print("test button")
# 添加输入引脚电平变化的回调函数
GPIO.add_event_detect(swi, GPIO.BOTH, callback=switch, bouncetime=200)
# 开启循环
while True:
    pass


