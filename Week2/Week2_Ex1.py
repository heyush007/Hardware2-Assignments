from filefifo import Filefifo


# Initialize data reader
data_reader = Filefifo(10, name='capture_250Hz_01.txt')

# Constants
SAMPLE_RATE = 250  # 250Hz sampling rate
TIME_PER_SAMPLE = 1 / SAMPLE_RATE 

# Variables
previous_value = None
previous_slope = 0
samples_between_peaks = 0
peak_intervals = []
is_first_peak_detected = False

def is_peak(previous_slope, current_slope):
    """Returns True when the slope changes from positive to negative (local peak)."""
    return previous_slope > 0 and current_slope <= 0

def calculate_frequency(peak_intervals):
    """Calculates mean peak-to-peak interval and frequency."""
    if len(peak_intervals) == 0:
        print("No peaks detected.")
        return

    avg_samples = sum(peak_intervals) / len(peak_intervals)
    avg_time = avg_samples * TIME_PER_SAMPLE
    frequency = 1 / avg_time if avg_time > 0 else 0

    print("\nPeak-to-peak intervals (in samples):", peak_intervals)
    print(f"Average peak-to-peak interval: {avg_samples:.2f} samples")
    print(f"Average peak-to-peak time: {avg_time:.4f} seconds")
    print(f"Estimated Frequency: {frequency:.2f} Hz\n")

# Read and process data
while data_reader.has_data() and len(peak_intervals) < 3:
    previous_value = data_reader.get()
    break

while data_reader.has_data() and len(peak_intervals) < 3:
    current_value = data_reader.get()
    samples_between_peaks += 1  # Count samples between peaks

    # Compute slope
    slope = current_value - previous_value

    # Detect peak
    if is_peak(previous_slope, slope):
        if is_first_peak_detected:  # If we already detected the first peak
            peak_intervals.append(samples_between_peaks)
            samples_between_peaks = 0  # Reset sample count between peaks
        is_first_peak_detected = True  # Mark first peak found

    previous_value = current_value
    previous_slope = slope

# Display results
calculate_frequency(peak_intervals)