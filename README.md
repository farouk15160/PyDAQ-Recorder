# DT-OPEN LAYERS PYTHON DATA LOGGER & PLOTTER

DESCRIPTION
-----------
This Python application interfaces with Data Translation (DT) USB DAQ boards 
(specifically targeted for DT9816) using the Open Layers API (oldaapi64.dll).

It performs the following actions:
1. Connects to the DAQ board via USB.
2. Logs Analog Input data from specified channels to a CSV file.
3. Handles real-time data conversion (Codes to Volts).
4. Upon stopping (Ctrl+C), generates a Matplotlib graph of active channels.
5. Allows the user to name channels dynamically before plotting.

PREREQUISITES
-------------
1. Hardware:
   - Data Translation USB DAQ Device (e.g., DT9816).
   - Connected via USB.

2. Drivers:
   - You must install the "DT-Open Layers" Driver suite (OMNI CD).
   - Download: https://digilent.com/reference/software/dt-open-layers/start
   - Ensure 'oldaapi64.dll' is present in C:\Windows\System32\ after install.

3. Python Environment:
   - Python 3.8 or higher (64-bit version required to match oldaapi64.dll).

INSTALLATION
------------
1. Install the required Python libraries:
   
   pip install pandas matplotlib

2. Verify the driver installation:
   Ensure "oldaapi64.dll" exists in C:\Windows\System32.

CONFIGURATION
-------------
Open the Python script and adjust the constants at the top if necessary:

- CHANNELS: List of channel indices to record (e.g., [0, 1, 2]).
- FREQ_HZ:  Sampling frequency (samples per second).
            * Note: To record 1 sample per minute, set FREQ_HZ = 1/60.
- GAIN:     Input gain setting (Specific to your board's capability).
- BOARD_NAME: Default is b"DT9816(00)". Change this if using a different model.

USAGE
-----
1. Run the script via command line:
   
   python main.py

2. The script will print board specifications and begin logging.
   The terminal will show: "Data: [Timestamp, Voltage, Voltage...]"

3. To STOP recording:
   Press [Ctrl] + [C] on your keyboard.

4. Post-Processing:
   - The script will detect channels with a mean voltage > 0.2V.
   - It will ask you to name these channels in the Terminal.
   - Example input: "Pressure_Sensor_1"
   - After naming, the plot window will open.
   - The data is saved to a file named "daq_log_YYYY-MM-DD_HH-MM-SS.csv".

TROUBLESHOOTING
---------------
Error: "Could not load 'oldaapi64.dll'"
   -> The driver is not installed, or you are using 32-bit Python with 64-bit 
      drivers (or vice versa). Ensure you are using 64-bit Python.

Error: "Driver Error..."
   -> Ensure the USB board is plugged in.
   -> Ensure the BOARD_NAME in the code matches your device name in the 
      Open Layers Control Panel.

Graph does not appear:
   -> The script ignores channels with an average voltage < 0.2V to filter noise.
      Ensure your sensors are active.

==============================================================================
