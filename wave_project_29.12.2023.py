 """
 * Wave generator
 *
 *  Created on: Dec 10, 2023
 *      Author: majorBien
 """

from machine import Pin,SPI,PWM,ADC
import framebuf
import time
import utime

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    
    def clear(self, color=0x0000):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)

        # Clear the buffer with the specified color
        for _ in range(self.width * self.height):
            self.spi.write(bytearray([color >> 8, color & 0xFF]))

        self.cs(1)

 
        
    



        
   
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    #color BRG
    LCD.fill(LCD.white)
 
    LCD.show()
    LCD.text("Extrime Design Custom",40,40,LCD.blue)
    LCD.text("Turbo wave",75,60,LCD.blue)
    LCD.text("Alfa",100,80,LCD.blue)
    
    
    
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)
    
    

    
    LCD.show()
    #----------------------init GPIO---------------------------
    key0 = Pin(15,Pin.IN,Pin.PULL_UP)
    key1 = Pin(17,Pin.IN,Pin.PULL_UP)
    key2 = Pin(3,Pin.IN,Pin.PULL_UP)
    servo_pin = 18
    pwm = machine.PWM(servo_pin)
    pwm.freq(50)
    adc = ADC(1)
   #----------------------------------------------------------
   
    LCD.show()
    time.sleep(1)
    LCD.clear()
    time.sleep(1)
    
    
    
    LCD.fill(0xFFFF)
    #visualisation variables
    level = 60
    level_string = "0"
    mode = "STOP"
    battery = 0
    #help variables
    flag1 = 0
    mode_int = 0
    adc_min = 0
    adc_max = 65535
    percent_min = 0
    percent_max = 100
    last_percent_value = -1
while True:
    
    if level > 100:
        level = 100
    if level < 60:
        level = 60
        
        
    #level_string = str(level)
    if level == 60:
        level_string = "0"
    if level == 70:
        level_string = "1"
    if level == 80:
        level_string = "2"
    if level == 90:
        level_string = "3"
    if level == 100:
        level_string = "4"
    battery_string = str(battery)
    
    
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)
    LCD.text("Wave level:",75,40,LCD.blue)
    LCD.text(level_string,165,40,LCD.blue)
   
    LCD.text("Mode:",85,60,LCD.blue)
    LCD.text(mode, 125,60,LCD.blue)
    LCD.text("Battery:",80,80,LCD.blue)
    LCD.text(battery_string,145,80,LCD.blue)
    if battery > 9 and battery < 100:
         LCD.text("%",162,80,LCD.blue)
    elif battery == 100:
         LCD.text("%",169,80,LCD.blue)
    else:
         LCD.text("%",153,80,LCD.blue)

    if key0.value() == 0 :
        time.sleep(0.1)
        level += 10
        LCD.fill(LCD.white)
        
    if key1.value() == 0:
        time.sleep(0.1)
        level -= 10
        
        LCD.fill(LCD.white)
    if key2.value() == 0:
        mode_int +=1
        time.sleep(0.1)
    if mode_int > 1:
        mode_int = 0
        
    if mode_int == 0 and key2.value() == 0:
        LCD.fill(LCD.white)
        mode = "STOP"
        
    elif mode_int == 1 and key2.value() == 0:
        LCD.fill(LCD.white)
        mode = "RUN"
        
    
    LCD.show()
    rotation = (level / 100) * 200

    
    if mode == "RUN":
        pulse_width = int((rotation / 180.0 * 1000) + 500)
        pwm.duty_ns(pulse_width * 1000)
    if mode == "STOP":
        level = 60
        pulse_width = int((rotation / 180.0 * 1000) + 500)
        pwm.duty_ns(pulse_width * 1000)
        
    adc_value = adc.read_u16()
    battery = int(((adc_value - adc_min) / (adc_max - adc_min)) * (percent_max - percent_min) + percent_min)
    
    #battery = max(min(percent_value, 100), 0)
    if battery != last_percent_value:
          LCD.fill(LCD.white)
          last_percent_value = battery
          
    
