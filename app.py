CHANNELS = [0,1,2,3,4,5] #   
GAIN = 0.1  # wird hier mit Faktor 10 multipliziert
FREQ_HZ = 20 # Aufnahmen per Sekunde ändern auf 1/60 dann hat man eine Aufnahem per minute


import ctypes
import time
import csv
import sys
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt



try:
    dll = ctypes.CDLL("oldaapi64.dll")
except OSError: 
    try:
        dll = ctypes.CDLL(r"C:\Windows\System32\oldaapi64.dll")
    except OSError:
        print("CRITICAL ERROR: Could not load 'oldaapi64.dll'.")
        print("Please install the DT-Open Layers Drivers (OMNI CD) from Digilent/MCC.")
        sys.exit(1)

OLSS_AD = 0               # Analog Input Subsystem
OL_DF_SINGLEVALUE = 801   # Single Value Polling Mode

def check_err(ret, func, args):
    if ret != 0:
        raise RuntimeError(f"Driver Error {ret} in {func.__name__}")
    return args

dll.olDaInitialize.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
dll.olDaInitialize.restype = ctypes.c_int
dll.olDaInitialize.errcheck = check_err

dll.olDaGetDASS.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_void_p)]
dll.olDaGetDASS.restype = ctypes.c_int
dll.olDaGetDASS.errcheck = check_err

dll.olDaConfig.argtypes = [ctypes.c_void_p]
dll.olDaConfig.restype = ctypes.c_int
dll.olDaConfig.errcheck = check_err

dll.olDaSetDataFlow.argtypes = [ctypes.c_void_p, ctypes.c_uint]
dll.olDaSetDataFlow.restype = ctypes.c_int
dll.olDaSetDataFlow.errcheck = check_err

dll.olDaGetSingleValue.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_long), ctypes.c_uint, ctypes.c_double]
dll.olDaGetSingleValue.restype = ctypes.c_int
dll.olDaGetSingleValue.errcheck = check_err

dll.olDaCodeToVolts.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_uint, ctypes.c_uint, ctypes.c_long, ctypes.POINTER(ctypes.c_double)]
dll.olDaCodeToVolts.restype = ctypes.c_int
dll.olDaCodeToVolts.errcheck = check_err

dll.olDaGetRange.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
dll.olDaGetResolution.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
dll.olDaGetEncoding.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]

dll.olDaReleaseDASS.argtypes = [ctypes.c_void_p]
dll.olDaTerminate.argtypes = [ctypes.c_void_p]



def plot_data(filename, channels):
    print("\n--- Generating Plot ---")

    try:
        df = pd.read_csv(filename)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        titles_names=[]
        valid_channels = []
        for ch in channels:
            col_name = f"Ch{ch} (V)"
            if col_name in df.columns:
                if df[col_name].mean() > 0.2:
                    user_input=str(input(f"Gebe die Names des Channel Nummer {ch} ein: "))
                    titles_names.append(user_input)
                    valid_channels.append(ch)
                    # add CSV dataheader naming, remove unsed data, add a GUI 

        if len(valid_channels) == 0:
            print("No channels exceed mean > 0.2 V. Nothing to plot.")
            return
        fig, axes = plt.subplots(len(valid_channels), 1,
                                 figsize=(12, 3 * len(valid_channels)),
                                 sharex=True)
        if len(valid_channels) == 1:
            axes = [axes]
        for i, ch in enumerate(valid_channels):
            ax = axes[i]
            col_name = f"Ch{ch} (V)"

            ax.plot(df['Timestamp'], df[col_name], label=f"Channel {ch}")
            ax.set_title(f"Channel {ch+1} Voltage {titles_names[i]}")
            ax.set_ylabel("Voltage (V)")
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend(loc="upper right")

        axes[-1].set_xlabel("Time")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Could not plot data: {e}")

BOARD_NAME = b"DT9816(00)" 
FILENAME = f"daq_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

def main():
    print(f"--- Initializing {BOARD_NAME.decode()} ---")
    
    hdev = ctypes.c_void_p()
    hdass = ctypes.c_void_p()

    try:
        dll.olDaInitialize(BOARD_NAME, ctypes.byref(hdev))
        dll.olDaGetDASS(hdev, OLSS_AD, 0, ctypes.byref(hdass))
        dll.olDaSetDataFlow(hdass, OL_DF_SINGLEVALUE)
        dll.olDaConfig(hdass)

        min_v = ctypes.c_double()
        max_v = ctypes.c_double()
        res_bits = ctypes.c_uint()
        encoding = ctypes.c_uint()
        
        dll.olDaGetRange(hdass, ctypes.byref(max_v), ctypes.byref(min_v))
        dll.olDaGetResolution(hdass, ctypes.byref(res_bits))
        dll.olDaGetEncoding(hdass, ctypes.byref(encoding))
        
        print(f"Specs: {res_bits.value}-bit, Range [{min_v.value}V to {max_v.value}V]")
        print(f"Logging Channels {CHANNELS} to {FILENAME}")
        print("Press Ctrl+C to STOP recording and VIEW PLOT.")

        with open(FILENAME, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp"] + [f"Ch{ch} (V)" for ch in CHANNELS])

            while True:
                row = [datetime.now().isoformat()]
                
                for ch in CHANNELS:
                    raw_val = ctypes.c_long()
                    volts = ctypes.c_double()
                    
                    dll.olDaGetSingleValue(hdass, ctypes.byref(raw_val), ch, GAIN)
                    
                    dll.olDaCodeToVolts(
                        min_v, max_v, GAIN, res_bits, encoding, 
                        raw_val, ctypes.byref(volts)
                    )
                    row.append(round(volts.value, 5))

                writer.writerow(row)
                print(f"Data: {row[1:]}") 
                time.sleep(1.0 / FREQ_HZ)

    except KeyboardInterrupt:
        print("\nStopping acquisition...")

    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        if hdass: dll.olDaReleaseDASS(hdass)
        if hdev: dll.olDaTerminate(hdev)
        print("Hardware released.")
        
        plot_data(FILENAME, CHANNELS)

if __name__ == "__main__":
    main()
