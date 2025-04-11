from machine import Pin, I2C
import time
from ssd1306 import SSD1306_I2C

t= 50
# OLED Setup
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# LED Pins
led1 = Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(22, Pin.OUT)

# Rotary Encoder Pins 
clk = Pin(10, Pin.IN, Pin.PULL_UP) #Clock pin
dt = Pin(11, Pin.IN, Pin.PULL_UP)  #Data Pin
sw = Pin(12, Pin.IN, Pin.PULL_UP)  #Button Switch Pin

# State using a closure
def create_state():
    selected_led = 0  #0 for LED1, 1 for LED2, 2 for LED3
    led1_on = 0
    led1_on = 0
    led2_on = 0
    led3_on = 0
    event = 0   #0: no event, 1: rotation, 2: button press
    last_clk = clk.value()
    last_press_time = time.ticks_ms() # Track time of last press for debounce

    def get():
        return selected_led, led1_on, led2_on, led3_on, event, last_clk, last_press_time

    def set(sel=None, s1=None, s2=None, s3=None, e=None, clk_val=None, press_time=None):
        nonlocal selected_led, led1_on, led2_on, led3_on, event, last_clk, last_press_time
        if sel is not None: selected_led = sel
        if s1 is not None: led1_on = s1
        if s2 is not None: led2_on = s2
        if s3 is not None: led3_on = s3
        if e is not None: event = e
        if clk_val is not None: last_clk = clk_val
        if press_time is not None: last_press_time = press_time

    def clear_event():
        nonlocal event
        event = 0

    return get, set, clear_event

get_state, set_state, clear_event = create_state()

# OLED Update 
def update_display():
    selected_led, led1_on, led2_on, led3_on, *_ = get_state()

    oled.fill(0) 

    # Helper to format a line
    def format_line(index, is_on, selected):
        if selected:
            return f"[LED{index + 1} - {'ON ' if is_on else 'OFF'}]"
        else:
            return f" LED{index + 1} - {'ON ' if is_on else 'OFF'}"

    oled.text(format_line(0, led1_on, selected_led == 0), 0, 0)
    oled.text(format_line(1, led2_on, selected_led == 1), 0, 12)
    oled.text(format_line(2, led3_on, selected_led == 2), 0, 24)

    oled.show()

# Rotary Interrupt Handler
def rotary_handler(pin):
    selected_led, l1, l2, l3, event, last_clk, last_press = get_state()
    new_clk = clk.value()

    if new_clk != last_clk:
        if dt.value() != new_clk:
            selected_led = (selected_led + 1) % 3  # Clockwise
        else:
            selected_led = (selected_led - 1) % 3  # Anticlockwise
        set_state(sel=selected_led, e=1)  # Mark event = 1 (rotation)

    set_state(clk_val=new_clk)  # Update last CLK value

# Button Press Interrupt Handler with debounce 
def button_handler(pin):
    selected_led, l1, l2, l3, event, last_clk, last_press = get_state()
    now = time.ticks_ms()

    # Ignore presses that are too close together
    if time.ticks_diff(now, last_press) > t:
        set_state(e=2, press_time=now)

# Attach Interrupts 
clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=rotary_handler)
sw.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# Show Initial Menu 
update_display()

# Main Loop
while True:
    selected_led, l1, l2, l3, event, *_ = get_state()

    if event == 1:
        # Encoder turned: just update the display
        update_display()
        clear_event()

    elif event == 2:
        # Button pressed: toggle selected LED
        if selected_led == 0:
            l1 = 1 - l1  # Toggle LED1
            led1.value(l1)
        elif selected_led == 1:
            l2 = 1 - l2  # Toggle LED2
            led2.value(l2)
        elif selected_led == 2:
            l3 = 1 - l3  # Toggle LED3
            led3.value(l3)

        # Save updated states and refresh display
        set_state(s1=l1, s2=l2, s3=l3)
        update_display()
        clear_event()
