import time
import sensor, image

from pyb import UART
import pyb

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
#sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # can be QVGA on M7...
sensor.skip_frames(30)
sensor.set_auto_gain(False) # must turn this off to prevent image washout...
clock = time.clock()
ir_led = pyb.LED(4)

#red   = (18, 50, 17, 50, -12, 97)
#green = (6, 39, -59, -13, -128, 127)
#blue   =  (5, 100, -109, 15, -50, -1)

thresholds = [(36, 59, 30, 91, 1, 93), # generic_red_thresholds -> index is 0 so code == (1 << 0)
              (34, 67, -65, -22, -30, 24),
              (33, 54, -14, 18, -62, -21)] # generic_green_thresholds -> index is 1 so code == (1 << 1)
# 当“find_blobs”的“merge = True”时，code代码被组合在一起。

uart = pyb.UART(3,115200)
uart.init(115200,bits=8,parity=None,stop=1)

a = 0
QR_buf=0
i=0
QR_flag=0
times = 0
times_js = 5
order = 0

def compareBlob(blob1,blob2):
    tmp = blob1.pixels() - blob2.pixels()
    if tmp == 0:
      return 0;
    elif tmp > 0:
      return 1;
    else:
      return -1;



while(True):
    clock.tick()
    img = sensor.snapshot()
    if uart.any():
       a = uart.readchar()
       a = a - 48
       if(a==1):
          order = 1
          print(order)
    if(order==0):
       #sensor.set_pixformat(sensor.RGB565)
       #img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.
       for code in img.find_qrcodes():
              img.draw_rectangle(code.rect(), color = (255, 0, 0))
              QR_buf = code.payload()
              if(QR_buf != 0):
                   print(QR_buf)
                   if(QR_buf=="123"):
                          uart.write("123\r\n\r")
                   elif(QR_buf=="132"):
                         uart.write("132\r\n\r")
                   elif(QR_buf=="213"):
                        uart.write("213\r\n\r")
                   elif(QR_buf=="231"):
                         uart.write("231\r\n\r")
                   elif(QR_buf=="312"):
                        uart.write("312\r\n\r")
                   elif(QR_buf=="321"):
                        uart.write("321\r\n\r")
    else:
         ir_led.on()
         sensor.set_pixformat(sensor.RGB565)
         for blob in img.find_blobs(thresholds,roi=(0,0,320,240),margin=2, pixels_threshold=20, area_threshold=5000, merge=True):
                img.draw_rectangle(blob.rect())
                img.draw_cross(blob.cx(), blob.cy())
                if blob.code()==1:
                   print(blob.code())
                   uart.write("001\r\n\r")
                elif blob.code()==2:
                   print(blob.code())
                   uart.write("002\r\n\r")
                elif blob.code()==4:
                   print(blob.code())
                   uart.write("003\r\n\r")
                else:
                   pass
