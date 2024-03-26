from picamera2 import Picamera2, Preview
from gpiozero import MotionSensor
import time
import smbus
import datetime as dt
from picamera2.encoders import H264Encoder
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def motion_detected():
    global motion
    motion = True

def write_to_file():
    global state
    file1 = open("/home/class380/Desktop/dataFinal/systemStatus.txt", "a")
    temperature = readTemperature()
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file1.write(current_time + "," + str(temperature) + "," + state + "\n")
    file1.close()

class python_switch:
    def CAMERA_MOTION(self):
        global motion
        global state
        global millis
        pir.wait_for_motion(timeout = 10)
        pir.when_motion = motion_detected
        if(motion):
            current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            temperature = readTemperature()
            
            picam.start()
            
            camera_delay = millis()
            #wait two seconds pir has wider view then camera
            while(millis()-camera_delay < 2000):
                pass
            
            picam.capture_file("/home/class380/Desktop/dataFinal/" + str(current_time) + "_" + str(temperature) + ".jpg")
            picam.stop()
            motion = False
            
            
            i= Image.open(r"/home/class380/Desktop/dataFinal/" + str(current_time) + "_" + str(temperature) + ".jpg")
            
            draw = ImageDraw.Draw(i)
            draw.rectangle(((15,10),(620,37)), fill = 'white')
            font = ImageFont.truetype("/opt/Wolfram/WolframEngine/13.1/SystemFiles/Fonts/TrueType/ClearSans-Thin.ttf", 20)
            draw.text((15, 10), str(current_time) + "_" + str(temperature), fill ="black", font = font, align ="right")
            #i.show()
            i.save("/home/class380/Desktop/dataFinal/" + str(current_time) + "_" + str(temperature) + ".jpg")
            i.close()
            
            
            pir.wait_for_no_motion()
        temperature = readTemperature()
        if(temperature <= 6):
            state = "TEMP" 
            write_to_file()
            
        
    def TEMP(self):
        global mySwitch
        global state
        temperature = readTemperature()
        if (temperature > 8):
            state = "CAMERA_MOTION"
            write_to_file()
            


def readTemperature():
    I2C_BUS = 1
    bus = smbus.SMBus(I2C_BUS)
    DEVICE_ADDRESS = 0x48
    
    temp_12bit = bus.read_word_data(DEVICE_ADDRESS,0)
    temp_low = (temp_12bit & 0xff00) >> 8
    temp_high = (temp_12bit & 0x00ff)
    temp = (((temp_high * 256)+ temp_low) >> 4)
    #handles negative temperatures
    if temp > 0x7FF:
        temp = temp - 4096
    temp = float(temp) * 0.0625
    temp = temp * 9/5 + 32
    return temp
    

def setup():
    print("in setup")
    global millis
    global state
    global picam
    global pir
    global motion
    
    millis = lambda: int(round(time.time() * 1000))
    state = "CAMERA_MOTION"
    picam = Picamera2()
    pir = MotionSensor(17)
    motion = False
    write_to_file()    


def loop():
    while True:
        global mySwitch
            
        mySwitch  = python_switch()
        
        if(state == "CAMERA_MOTION"):
            mySwitch.CAMERA_MOTION()         
        elif(state == "TEMP"):
            mySwitch.TEMP()
        

    
def destroy():
    print("in destroy")
    
    
if __name__=='__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
