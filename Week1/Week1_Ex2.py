from machine import Pin, I2C
import ssd1306 

# OLED display dimensions
WIDTH = 128
HEIGHT = 64
LINE_HEIGHT = 10  
MAX_LINES = HEIGHT // LINE_HEIGHT  

# Initialize I2C and OLED display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# List to store text lines
lines = []

def update_display():

    oled.fill(0)  
    for i, line in enumerate(lines[-MAX_LINES:]):  
        oled.text(line, 0, i * LINE_HEIGHT)
    oled.show()

print("Enter text (Press Ctrl+C to exit):")

while True:
    try:
        text = input("> ")  
        lines.append(text)  
        
        # If lines exceed the screen, remove the oldest one (scrolling effect)
        if len(lines) > MAX_LINES:
            lines.pop(0)
        
        update_display() 
    except KeyboardInterrupt:
        print("\nExiting program.")
        break
