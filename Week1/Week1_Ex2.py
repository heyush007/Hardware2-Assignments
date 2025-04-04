from machine import Pin, I2C
import ssd1306

# OLED display dimensions
WIDTH = 128
HEIGHT = 64
LINE_HEIGHT = 12  
MAX_LINES = HEIGHT // LINE_HEIGHT

# Initialize I2C interface and OLED display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) 
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

def display_text(lines):
    oled.fill(0)  
    for index, line in enumerate(lines): 
        oled.text(line, 0, index * LINE_HEIGHT)
    oled.show()

def main():
    lines = [] 
    
    while True:
        user_input = input("Enter text: ")  
        lines.append(user_input)
        
        if len(lines) > MAX_LINES:
            del lines[0] 
        
        display_text(lines) 

main()


