from filefifo import Filefifo
import time
from array import array

sample_rate = 250  
time_interval_2s = 2  
time_interval_10s = 10  
data_file = 'capture_250Hz_01.txt'

data = Filefifo(10, name=data_file)

# Readings in 2 secs list way
#samples_2s = []
#for i in range(sample_rate * time_interval_2s):
#    sample = data.get()
#    samples_2s.append(sample)

# Including array
samples_2s = array('f', [0] * (sample_rate * time_interval_2s))
for i in range(sample_rate * time_interval_2s):
    samples_2s[i] = data.get()

# Find min and max from the 2 seconds of data
min_value = min(samples_2s)
max_value = max(samples_2s)

# Print the minimum and maximum values from the 2 seconds of data
print(f"Minimum value from the first 2 seconds: {min_value}")
print(f"Maximum value from the first 2 seconds: {max_value}")

# Reading 10 seconds of data for plotting
#samples_10s = []
#for i in range(sample_rate * time_interval_10s):
#    sample = data.get()
#    samples_10s.append(sample)

# Including array
samples_10s = array('f', [0] * (sample_rate * time_interval_10s))
for i in range(sample_rate * time_interval_10s):
    samples_10s[i] = data.get()

# Scale the 10 seconds of data
#scaled_samples_10s = []
#for sample in samples_10s:
#    scaled_value = (sample - min_value) / (max_value - min_value) * 100
#    scaled_samples_10s.append(scaled_value)

# Including array 
scaled_samples_10s = array('f', [0] * len(samples_10s))
for i in range(len(samples_10s)):
    scaled_samples_10s[i] = (samples_10s[i] - min_value) / (max_value - min_value) * 100

# Print first 10 scaled values from the 10 seconds of data
print("\nScaled values for the first 10 seconds (0 to 100):")
for i in range(len(scaled_samples_10s)):
    print(f"{scaled_samples_10s[i]:.2f}")
