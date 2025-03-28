from machine import Pin, I2C
import ssd1306
import time

# OLED display dimensions
WIDTH = 128
HEIGHT = 64
MID_HEIGHT = HEIGHT // 2  # Middle of the screen

# Initialize I2C and OLED
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Button setup
SW0 = Pin(9, Pin.IN, Pin.PULL_UP)  
SW1 = Pin(8, Pin.IN, Pin.PULL_UP)  
SW2 = Pin(7, Pin.IN, Pin.PULL_UP)  

# Initial position
x = 0
y = MID_HEIGHT

# Drawing parameters
dx = 1 
dy = 2

def update_display(): 
    oled.pixel(x, y, 1)
    oled.show()

while True:
    if not SW2():
        y = max(0, y - dy)
    
    if not SW0(): 
        y = min(HEIGHT - 1, y + dy)
    
    if not SW1(): 
        x, y = 0, MID_HEIGHT
        oled.fill(0)
        oled.show()
        time.sleep(0.2)  # Debounce delay

    x += dx  

    if x >= WIDTH:  
        x = 0

    update_display()
    time.sleep(0.1)  
