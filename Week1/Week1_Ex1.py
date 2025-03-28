from machine import Pin, I2C
import ssd1306
import time

# OLED display dimensions
WIDTH = 128
HEIGHT = 32

# Initialize I2C and OLED
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Initialize buttons
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)  

# UFO settings
ufo = "<=>"
font_size = 8 
ufo_width = len(ufo) * font_size 
x_pos = 50 
y_pos = HEIGHT - font_size

def draw_ufo(x):
    oled.fill(0)  
    oled.text(ufo, x, y_pos)
    oled.show()

# Initial UFO display
draw_ufo(x_pos)

while True:
    if not sw0():
        if x_pos + ufo_width < WIDTH: 
            x_pos += font_size  
            draw_ufo(x_pos)
            time.sleep(0.1)
    
    if not sw2():  
        if x_pos > 0: 
            x_pos -= font_size  
            draw_ufo(x_pos)
            time.sleep(0.1)


