# GaitAnalysis

Detect gait events in walking data from the PhysioNet LTMM dataset.

## Dataset Overview

The [Long-Term Movement Monitoring (LTMM)](https://physionet.org/content/ltmm/1.0.0/) database contains 3-axis accelerometer recordings from older adults performing various activities including 1‑minute lab-based walking trials.

## Problem

This project demonstrates how to detect heel-strike events from accelerometer signals, compute stride metrics and compare gait characteristics between fallers and non‑fallers.

## Step-by-Step Plan

1. Load `.dat` and `.hea` files from the `LabWalks` directory.
2. Preprocess accelerometer signals (filter magnitude).
3. Detect heel‑strikes using peak detection.
4. Calculate stride time.
5. Compare fallers vs. non‑fallers using stride-time variability.
6. Plot and print results.

## Required Python Libraries

```bash
pip install numpy scipy matplotlib wfdb
```

## Potential Issues

- Raw data files must be downloaded separately from PhysioNet and placed in the expected `LabWalks` folder.
- The script assumes heel-strikes correspond to negative peaks in the filtered magnitude signal; tuning may be required for other datasets.
- Records with missing or corrupt channels may cause the loader to fail.
- Visualization depends on `matplotlib` which may require a display backend when running interactively.
