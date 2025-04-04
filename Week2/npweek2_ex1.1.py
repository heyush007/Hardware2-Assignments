from filefifo import Filefifo

# Read data from file
data = Filefifo(30, name='capture_250Hz_02.txt')

# Function to find positive peaks using slope inspection
def find_peaks(data):
    previous_value = data.get()  # Read the first sample
    sample_count = 0  # Start from the first sample
    peaks = []
    
    # Start processing from the second sample
    while True:
        current_value = data.get()  # Read next sample
        sample_count += 1

        # Ensure we have at least two samples to calculate the slope
        if sample_count > 1:
            slope = current_value - previous_value  # Calculate slope

            # Peak condition: previous slope was positive, now it's negative
            if slope < 0 and previous_slope > 0:
                peaks.append((sample_count - 1, previous_value))  # Save the previous sample as a peak

            previous_slope = slope  # Update slope for next iteration

        previous_value = current_value  # Update previous value for next iteration

        if sample_count > 2500:  # Limit number of samples
            break

    return peaks

# Function to print peak-to-peak intervals
def print_peak_to_peak(peaks):
    for i in range(1, len(peaks)):
        peak_1 = peaks[i - 1]
        peak_2 = peaks[i]
        interval = (peak_2[0] - peak_1[0]) / 250  # Convert sample count to seconds (250Hz rate)
        print(f"Peak {i}: Sample {peak_2[0]} (Time: {interval:.3f}s) - Interval from previous peak: {interval:.3f}s")

# Main function to find and print peaks
def main():
    peaks = find_peaks(data)
    print_peak_to_peak(peaks)

# Run the program
main()
