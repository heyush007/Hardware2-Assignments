from filefifo import Filefifo
import time
data = Filefifo(10, name = 'capture_250Hz_01.txt')
for _ in range(100):
    print(data.get())
    time.sleep(0.1)