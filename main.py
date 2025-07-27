import os
from typing import Tuple, Dict

import numpy as np
import wfdb
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt


def load_accel(file_path: str) -> Tuple[np.ndarray, float]:
    """Load 3-axis accelerometer data from a WFDB record.

    Parameters
    ----------
    file_path : str
        Path to the WFDB record without extension (e.g., ``LabWalks/CO001``).

    Returns
    -------
    acc_xyz : np.ndarray
        Array of shape (n_samples, 3) containing X, Y, Z accelerometer signals.
    fs : float
        Sampling frequency in Hz.
    """
    dat_path = f"{file_path}.dat"
    hea_path = f"{file_path}.hea"
    if not os.path.exists(dat_path) or not os.path.exists(hea_path):
        raise FileNotFoundError(
            f"Missing record files: {dat_path} or {hea_path}"
        )

    record = wfdb.rdrecord(file_path)
    acc_xyz = record.p_signal[:, :3]
    fs = float(record.fs)
    return acc_xyz, fs


def bandpass(
    signal: np.ndarray,
    fs: float,
    low: float = 0.5,
    high: float = 5,
) -> np.ndarray:
    """Bandpass filter a signal using a Butterworth filter."""
    nyquist = fs / 2.0
    b, a = butter(4, [low / nyquist, high / nyquist], btype="band")
    return filtfilt(b, a, signal)


def compute_magnitude(acc_xyz: np.ndarray) -> np.ndarray:
    """Compute signal magnitude vector from 3-axis accelerometer."""
    return np.linalg.norm(acc_xyz, axis=1)


def detect_heel_strikes(signal: np.ndarray, fs: float) -> np.ndarray:
    """Detect heel-strike events using peak detection on the
    inverted signal."""
    min_distance = int(0.5 * fs)  # at least 0.5 s between steps
    peaks, _ = find_peaks(-signal, distance=min_distance)
    return peaks


def compute_stride_features(
    peaks: np.ndarray, fs: float
) -> Tuple[Dict[str, float], np.ndarray]:
    """Compute stride-based gait features from heel-strike peak indices."""
    if len(peaks) < 2:
        return {
            "mean_stride_time": np.nan,
            "std_stride_time": np.nan,
            "step_frequency": np.nan,
        }, np.array([])

    stride_times = np.diff(peaks) / fs
    mean_stride = float(np.mean(stride_times))
    std_stride = float(np.std(stride_times))
    step_freq = 1.0 / mean_stride if mean_stride > 0 else np.nan

    features = {
        "mean_stride_time": mean_stride,
        "std_stride_time": std_stride,
        "step_frequency": step_freq,
    }
    return features, stride_times


def plot_gait(filtered_mag: np.ndarray, peaks: np.ndarray, fs: float) -> None:
    """Plot filtered magnitude with detected heel strikes."""
    times = np.arange(len(filtered_mag)) / fs
    plt.figure(figsize=(10, 4))
    plt.plot(times, filtered_mag, label="Filtered |Acc|")
    plt.plot(times[peaks], filtered_mag[peaks], "ro", label="Heel-strike")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (g)")
    plt.title("Heel-strike Detection")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    record = "LabWalks/CO001"
    try:
        accel, fs = load_accel(record)
    except FileNotFoundError as exc:
        print(f"Error loading record {record}: {exc}")
    else:
        magnitude = compute_magnitude(accel)
        filtered = bandpass(magnitude, fs)
        heel_peaks = detect_heel_strikes(filtered, fs)
        features, strides = compute_stride_features(heel_peaks, fs)

        print(f"Mean stride time: {features['mean_stride_time']:.3f} s")
        print(f"Stride time SD: {features['std_stride_time']:.3f} s")
        print(f"Step frequency: {features['step_frequency']:.3f} steps/s")

        plot_gait(filtered, heel_peaks, fs)
