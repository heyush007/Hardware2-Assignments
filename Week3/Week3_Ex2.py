from machine import Pin, I2C
import time
from ssd1306 import SSD1306_I2C
import array

# OLED Setup (I2C)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000) 
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Define LED pins
led_pins = array.array('I', [2, 3, 4])  
led_states = array.array('b', [0, 0, 0])

# Rotary Encoder Pins
clk = Pin(10, Pin.IN, Pin.PULL_UP)  
dt = Pin(11, Pin.IN, Pin.PULL_UP)   
sw = Pin(12, Pin.IN, Pin.PULL_UP)   

# Variables
menu_index = 0
last_clk_state = clk.value()
last_press_time = 0  # Debounce timing

event_fifo = array.array('b', [0])  # FIFO buffer

def rotary_interrupt(pin):
    global menu_index, last_clk_state
    new_clk_state = clk.value()
    
    if new_clk_state != last_clk_state:
        if dt.value() != new_clk_state:
            menu_index = (menu_index + 1) % 3  # Wrap around
        else:
            menu_index = (menu_index - 1) % 3
        event_fifo[0] = 1
    last_clk_state = new_clk_state

def button_interrupt(pin):
    global last_press_time
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press_time) > 50:
        event_fifo[0] = 2
        last_press_time = current_time

# Attach interrupts
clk.irq(trigger=Pin.IRQ_FALLING, handler=rotary_interrupt)
sw.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt)

def update_oled():
    oled.fill(0)
    for i in range(3):
        indicator = "->" if i == menu_index else "  "
        status = "ON" if led_states[i] else "OFF"
        oled.text(f"{indicator} LED{i+1}: {status}", 10, i * 12)
    oled.show()

def toggle_led():
    led_states[menu_index] = 1 - led_states[menu_index]
    Pin(led_pins[menu_index], Pin.OUT).value(led_states[menu_index])

# Initialize OLED
time.sleep(1)
update_oled()

# Main loop
while True:
    if event_fifo[0] != 0:
        event = event_fifo[0]
        event_fifo[0] = 0
        if event == 1:
            update_oled()
        elif event == 2:
            toggle_led()
            update_oled()
