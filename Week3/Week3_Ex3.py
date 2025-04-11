from machine import Pin, I2C
import time
from ssd1306 import SSD1306_I2C
import array

# --- OLED Setup ---
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

data_file = 'capture_250Hz_02.txt'

# --- Rotary Encoder Pins ---
clk = Pin(10, Pin.IN, Pin.PULL_UP)
dt = Pin(11, Pin.IN, Pin.PULL_UP)
sw = Pin(12, Pin.IN, Pin.PULL_UP)

# --- Filefifo Class ---
class Filefifo:
    def __init__(self, size, file_name):
        self.size = size
        self.buffer = []
        self.file_name = file_name
        self._load_file()

    def _load_file(self):
        with open(self.file_name, 'r') as file:
            for line in file:
                self.buffer.append(int(line.strip()))

    def get(self):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)  # Return and remove the first element in FIFO

    def peek(self):
        if len(self.buffer) > 0:
            return self.buffer[0]  # Peek at the first element without removing it

    def is_empty(self):
        return len(self.buffer) == 0

# --- File data loading ---
fifo_data = Filefifo(10, data_file)

# --- Variables ---
current_index = 0
data_window = [0] * 128  # Empty window of 128 samples
event = 0  # Used to track events

# --- State handling ---
def set_state(index=None, clk_val=None):
    global current_index
    if index is not None:
        current_index = index

# --- Rotary Interrupt Handler ---
def rotary_handler(pin):
    global data_window
    new_clk = clk.value()

    # Detect a change in encoder value
    if new_clk != clk.value():
        if dt.value() != new_clk:
            # Rotate counter-clockwise: decrease index
            current_index = max(0, current_index - 1)
        else:
            # Rotate clockwise: increase index
            current_index = min(len(fifo_data.buffer) - 128, current_index + 1)
        
        # Update the data window
        data_window = fifo_data.buffer[current_index:current_index + 128]
        event = 1  # Indicate a rotary turn has happened
        update_display()  # Update the display immediately

# --- Button Press Interrupt Handler ---
def button_handler(pin):
    global event
    event = 2  # Button pressed event

# Attach interrupts
clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=rotary_handler)
sw.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# --- OLED Update ---
def update_display():
    oled.fill(0)
    # Display current data window
    for i in range(128):
        oled.text(str(data_window[i]), 0, i * 5)
    oled.show()

# --- Main Loop ---
while True:
    if event == 1:  # Rotary encoder turn detected
        event = 0  # Clear event

    elif event == 2:  # Button press detected
        # Handle button press action (e.g., toggle something)
        event = 0  # Clear event
