from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime
from time import sleep


i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

char_h = 8
char_w = 8

UFO = "<===>"
y= oled_height - char_h
step = 4

ufo_position = int((oled_width - (len(UFO) * char_w)) / 2)

sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)

def display_ufo(x):
    oled.fill(0)
    oled.text(UFO, x, y) 
    oled.show()

def is_button_pressed(button):
    return not button.value()

while True:
    if is_button_pressed(sw2):
        ufo_position -= step  
    elif is_button_pressed(sw0):
        ufo_position += step  


    if ufo_position < 0:
        ufo_position = 0
    elif ufo_position > (oled_width - len(UFO) * char_w):
        ufo_position = (oled_width - len(UFO) * char_w)
        
    display_ufo(ufo_position)