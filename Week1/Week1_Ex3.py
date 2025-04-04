from machine import Pin, I2C
import ssd1306
import utime

# OLED display dimensions
WIDTH = 128
HEIGHT = 64

# Button Pins
SW0 = 9  # Moves Down
SW1 = 8  # Clear Screen
SW2 = 7  # Moves Up 

# Initialize I2C interface and OLED display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Initialize buttons
btn_up = Pin(SW2, Pin.IN, Pin.PULL_UP)  
btn_clear = Pin(SW1, Pin.IN, Pin.PULL_UP)
btn_down = Pin(SW0, Pin.IN, Pin.PULL_UP)  

def draw_pixel(x, y):
    oled.pixel(x, y, 1)
    oled.show()

def clear_screen():
    oled.fill(0)
    oled.show()

def main():
    x = 0  # Start from the left edge
    y = HEIGHT // 2  # Middle of the screen
    clear_screen()
    
    while True:
        if not btn_up.value():  
            y = max(0, y - 1)  
            
        if not btn_down.value(): 
            y = min(HEIGHT - 1, y + 1)  
            
        if not btn_clear.value():
            x = 0
            y = HEIGHT // 2
            clear_screen()
        
        draw_pixel(x, y)
        
        x += 1
        if x >= WIDTH:
            x = 0  # Wrap around to the left

main()