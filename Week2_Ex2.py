from filefifo import Filefifo

SAMPLE_RATES =250

data = Filefifo(10, name = 'capture_250Hz_01.txt')

samples = [data.get() for _ in range(1000)]

peaks = []
for i in range(1, len(samples) - 1):
    if samples[i - 1] < samples[i] > samples[i + 1]: 
        peaks.append(i)

intervals = [peaks [i] - peaks [i-1] for i in range(1, len(peaks))]

 