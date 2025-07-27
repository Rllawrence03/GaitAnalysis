import numpy as np
import pandas as pd
import wfdb
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt

def load_accel(mit_path):
    record = wfdb.rdrecord(mit_path)
    acc = record.p_signal[:, :3]  # first 3 channels = X, Y, Z
    fs = record.fs
    ts = np.arange(len(acc)) / fs
    return ts, acc, fs

def bandpass(signal, fs, low=0.5, high=5):
    b, a = butter(3, [low/(fs/2), high/(fs/2)], btype='band')
    return filtfilt(b, a, signal)

def detect_gait_events(acc_signal, fs):
    mag = np.linalg.norm(acc_signal, axis=1)
    filtered = bandpass(mag, fs)
    peaks, _ = find_peaks(-filtered, prominence=0.2, distance=int(0.5*fs))
    stride_times = np.diff(peaks) / fs
    return peaks, stride_times, filtered

# Example usage
# Replace 'LabWalks/CO001' with the correct path to your downloaded record
ts, acc, fs = load_accel('LabWalks/CO001')
peaks, strides, filtered_mag = detect_gait_events(acc, fs)

print(f"Mean Stride Time: {np.mean(strides):.2f}s")
print(f"Stride Time Variability (SD): {np.std(strides):.2f}s")

plt.plot(ts, filtered_mag)
plt.plot(ts[peaks], filtered_mag[peaks], 'ro')
plt.title("Filtered Acc Magnitude with Heel-Strike Events")
plt.xlabel("Time (s)")
plt.ylabel("Filtered |Acc|")
plt.show()
