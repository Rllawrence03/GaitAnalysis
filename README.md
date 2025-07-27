# GaitAnalysis
Detect Gait events in walking data

from pathlib import Path

project_md = """
# Gait Event Detection from NIH LTMM Dataset (PhysioNet)

## 🧪 Dataset Overview

**Source**: [PhysioNet Long-Term Movement Monitoring (LTMM)](https://physionet.org/content/ltmm/1.0.0/)

- 3-axis accelerometer data from 71 older adults
- Includes **lab-based 1-minute walk trials**
- Objective: detect **gait events** (heel-strike, toe-off) and assess **stride time variability**

---

## 🎯 Problem

**Goal**:  
Detect heel-strike events during walking from accelerometer signals, calculate stride time variability, and **compare fallers vs non-fallers** using public data.

---

## ✅ Step-by-Step Plan

1. **Load .dat + .hea files** from LabWalks directory  
2. **Preprocess accelerometer signal** (low-pass filter, magnitude)  
3. **Detect heel-strikes** using peak detection  
4. **Calculate stride time**  
5. **Compare fallers vs non-fallers** using stride time SD  
6. **Plot and print results**

---

## 🧰 Required Python Libraries

```bash
pip install numpy pandas scipy matplotlib wfdb
