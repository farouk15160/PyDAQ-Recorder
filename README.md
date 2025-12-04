# 📊 PyDAQ-Logger: Data Translation Interface

A Python-based Data Acquisition & Logging tool for **Data Translation (MCC) Hardware**.

---

## 📖 Overview

PyDAQ-Logger provides a robust Python interface for Data Translation USB DAQ boards (tested on DT9816) using the **DT-Open Layers driver (oldaapi64.dll)**.

It handles:

* Hardware initialization
* Real-time voltage logging to CSV
* Automated post-acquisition visualization

---

## ✨ Features

* **Direct Driver Access:** Uses `ctypes` to wrap `oldaapi64.dll`, bypassing proprietary software.
* **Real-Time Logging:** Logs 6 analog channels to timestamped CSV.
* **Smart Visualization:** Detects active channels (Mean > 0.2V) and ignores floating pins.
* **Interactive Naming:** Prompts user for active channel names.
* **Robust Error Handling:** Gracefully releases hardware resources on Ctrl+C.

---

## 🛠️ Prerequisites

### Hardware

* Data Translation DAQ Board (DT9816)
* DT-Open Layers driver installed
* `oldaapi64.dll` in `C:\Windows\System32\` or script directory

### Software

* Python 3.8+
* Libraries:

```
pip install pandas matplotlib
```

---

## 🚀 Usage

### Connect Hardware

Plug in your USB DAQ board.

### Run the Script

```
python main.py
```

### Recording

* Initializes board and prints resolution & voltage range
* Logs to CSV: `daq_log_YYYY-MM-DD_HH-MM-SS.csv`
* Prints voltages to console

### Stop & Plot

* Press Ctrl+C
* Name active channels (e.g., `Pressure Sensor`)
* Stacked plot window appears

---

## ⚙️ Configuration

Adjust sampling parameters at the top of the script:

```python
CHANNELS = [0, 1, 2, 3, 4, 5]  # Active pins
GAIN = 0.1                     # Board-specific gain
FREQ_HZ = 20                   # Samples per second
```

Change to 1 sample per minute:

```python
FREQ_HZ = 1/60  # 0.0166 Hz
```

---

## 📊 Example Output

### Console

```
--- Initializing DT9816(00) ---
Specs: 16-bit, Range [-10.0V to 10.0V]
Logging Channels [0,1,2,3,4,5] to daq_log_2023-10-25_14-30-00.csv
Press Ctrl+C to STOP recording and VIEW PLOT.
Data: [0.0012, 4.9821, 0.0001, ...]
```

### CSV Structure

| Timestamp               | Ch0 (V) | Ch1 (V) | ... |
| :---------------------- | :------ | :------ | :-- |
| 2023-10-25T14:30:00.123 | 0.0012  | 4.9821  | ... |

---

## ⚠️ Troubleshooting

* **CRITICAL ERROR: Could not load 'oldaapi64.dll'**

  * Install manufacturer drivers
  * Ensure DLL is in System32 or script folder

* **Driver Error X in olDaInitialize**

  * Check board connection
  * Ensure no other program (QuickDAQ etc.) is using the board

---

## 📜 License

Open Source. Modify freely for your DAQ hardware implementation.
