import sensor, image, time
from pyb import UART
import json

#red_threshold_01 = ((35, 100, 41, 77, 24, 59));     # red
#green_threshold_01 = ((50, 100, -80, -20, 8, 20));  # green
#blue_threshold_01 = ((20, 100, -18, 18, -80, -30)); # blue

red_threshold_01 = (34, 61, 73, 43, 72, 10);        # red
green_threshold_01 = (34, 14, -64, -13, 13, -2);    # green
blue_threshold_01 = (6, 47, 56, -11, -63, -21);     # blue
#设置红色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,
# maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。如果是灰度图，则只需
#设置（min, max）两个数字即可。

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000 )
sensor.set_auto_whitebal(False)
#关闭白平衡。白平衡是默认开启的，在颜色识别中，需要关闭白平衡。

clock = time.clock()

uart = UART(3, 115200)

uart.init(115200, bits=8, parity=None, stop=1)  #8位数据位，无校验位，1位停止位、

while(True):
    clock.tick()
    img = sensor.snapshot()
    blob_red = img.find_blobs([red_threshold_01], area_threshold=150);
    blob_green = img.find_blobs([green_threshold_01], area_threshold=150);
    blob_blue = img.find_blobs([blue_threshold_01], area_threshold=150);
   # blob_red = img.find_blobs([red_threshold_01], pixels_threshold=100, area_threshold=100, merge=True, margin=10);      #红色物块
    #blob_green = img.find_blobs([green_threshold_01], pixels_threshold=100, area_threshold=100, merge=True, margin=10); #绿色物块
    #blob_blue = img.find_blobs([blue_threshold_01], pixels_threshold=100, area_threshold=100, merge=True, margin=10);   #蓝色物块
    if blob_red: #如果找到了目标颜色
        #FH = bytearray([0xA1,0xA1])
        #uart.write(FH) #输出的是帧头
        for b in blob_red:
        #迭代找到的目标颜色区域
            img.draw_rectangle(b[0:4]) # rect
            img.draw_cross(b[5], b[6]) # cx, cy
            x = b.cx()
            y = b.cy()
            print(x, y, end = ',')
            data = bytearray([0xA1,0xA1,x,y,0xA2])
            uart.write(data) #输出的是色块坐标位置信息
        #FH1 = bytearray([0xA2])
        #uart.write(FH1) #输出的是帧尾
        #uart.write("%x %x \r"%(x,y))
        #以16进制的格式输出，（16进制不能这样输出啊，浪费了我两天的时间）
    if blob_green: #如果找到了目标颜色
        #FH = bytearray([0xB2,0xB2])
        #uart.write(FH) #输出的是帧头
        for b in blob_green:
        #迭代找到的目标颜色区域
            img.draw_rectangle(b[0:4]) # rect
            img.draw_cross(b[5], b[6]) # cx, cy
            x = b.cx()
            y = b.cy()
            print(x, y, end = ',')
            data = bytearray([0xB2,0xB2,x,y,0xB3])
            uart.write(data) #输出的是色块坐标位置信息
        #FH1 = bytearray([0xB3])
        #uart.write(FH1) #输出的是帧尾
    if blob_blue: #如果找到了目标颜色
        #FH = bytearray([0xC3,0xC3])
        #uart.write(FH) #输出的是帧头
        for b in blob_blue:
        #迭代找到的目标颜色区域
            img.draw_rectangle(b[0:4]) # rect
            img.draw_cross(b[5], b[6]) # cx, cy
            x = b.cx()
            y = b.cy()
            print(x, y, end = ',')
            data = bytearray([0xC3,0xC3,x,y,0xC4])
            uart.write(data) #输出的是色块坐标位置信息
        #FH1 = bytearray([0xC4])
        #uart.write(FH1) #输出的是帧尾
    time.sleep(1000)
    #img.draw_circle((50, 50, 30), color = (250, 0, 0))


    print(clock.fps())
