from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

SAMPLE_RATE = 250  # Hz
Data_file = 'capture_250Hz_02.txt'

#i2c pin
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128,64, i2c)

# Read samples
data = Filefifo(10, name= Data_file)
samples = [data.get() for _ in range(1000)]

# Find positive peaks 
peaks = []
for i in range(1, len(samples) - 1):
    if samples[i - 1] < samples[i] > samples[i + 1]:
        peaks.append(i)
        
#Computing values
intervals = [peaks[i] - peaks[i-1] for i in range(1, len(peaks))]
time_intervals = [interval/SAMPLE_RATE for interval in intervals]

if time_intervals:
    avg_intervals = sum(time_intervals)/len(time_intervals)
else:
    avg_intervals = 0
    
if avg_intervals !=0:
    frequency = 1/ avg_intervals
else:
    frequency = 0

oled.fill(0)

# Display on OLED
oled.text("HRM Peaks", 0, 0)
oled.text("Intervals:", 0, 10)

# Show first 2 intervals (converted to ms)
for idx, interval in enumerate(time_intervals[:2]):
    oled.text(f"{int(interval * 1000)} ms", 0, 20 + (idx * 10))

# Display frequency
oled.text("Freq: {:.2f} Hz".format(frequency), 0, 45)

oled.show()