from filefifo import Filefifo
from array import array

# Constants
sample_rate = 250
data_file = 'capture_250Hz_02.txt'

# Load data and read samples
data = Filefifo(10, name=data_file)
samples = array('h',[data.get() for _ in range(1000)])

# Find peaks using slope inspection
peaks = array('i')
for i in range(1, len(samples) - 1):
    prev_slope = samples[i] - samples[i - 1]
    next_slope = samples[i + 1] - samples[i]
    
    # Check for slope turning from positive to negative
    if prev_slope > 0 and next_slope < 0:
        peaks.append(i)
        
if len(peaks) > 1:
    intervals = array('i', [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)])
    time_intervals = array('f', [interval / sample_rate for interval in intervals])
else:
    intervals = array('i')
    time_intervals = array('f')

# Frequency calculation
if time_intervals:
    avg_interval = sum(time_intervals) / len(time_intervals)
    frequency = 1 / avg_interval
else:
    frequency = None

# Print results coverting into lists
#print("Peak-to-peak intervals (samples):", list(intervals[:5]))
#print("Peak-to-peak intervals (seconds):", list(time_intervals[:5]))
#print("Estimated Frequency:", frequency, "Hz")

# Print results directly from arrays without converting to lists
print("Peak-to-peak intervals (samples):")
for i in range(min(3, len(intervals))):  
    print(intervals[i])

print("Peak-to-peak intervals (seconds):")
for i in range(min(3, len(time_intervals))):  
    print(time_intervals[i])

print("Estimated Frequency:", frequency, "Hz")