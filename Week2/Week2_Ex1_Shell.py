from filefifo import Filefifo
from array import array

# Constants
sample_rate = 250
data_file = 'capture_250Hz_02.txt'

# Load data and read samples
data = Filefifo(10, name=data_file)
samples = array('h',[data.get() for _ in range(1000)])

# Find positive peaks 
peaks = array('i')
for i in range(1, len(samples) - 1):
    if samples[i - 1] < samples[i] > samples[i + 1]:
        peaks.append(i)

#Computing values
intervals = array('i',[peaks[i] - peaks[i-1] for i in range(1, len(peaks))])
time_intervals = array('f',[interval/sample_rate for interval in intervals])

if time_intervals:
    avg_intervals = sum(time_intervals)/len(time_intervals)
else:
    avg_intervals = 0
    
if avg_intervals !=0:
    frequency = 1/ avg_intervals
else:
    frequency = None

# Print results
#print("Peak-to-peak intervals (samples):", list(intervals[:5]))
#print("Peak-to-peak intervals (seconds):", list(time_intervals[:5]))
#print("Estimated Frequency:", frequency, "Hz")

# Print results directly from arrays without converting to lists
print("Peak-to-peak intervals (samples):")
for i in range(min(5, len(intervals))):  
    print(intervals[i])

print("Peak-to-peak intervals (seconds):")
for i in range(min(5, len(time_intervals))):  
    print(time_intervals[i])

print("Estimated Frequency:", frequency, "Hz")