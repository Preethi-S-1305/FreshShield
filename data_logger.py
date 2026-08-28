import serial
import csv
import os
import re
from datetime import datetime

# ==========================================
# FRESHSHIELD PRO - DATA LOGGER
# ==========================================

PORT = "COM6"
BAUD_RATE = 9600

CSV_FILE = "FreshShield_Data.csv"


# ==========================================
# CONNECT TO ARDUINO
# ==========================================

print("Connecting to Arduino...")

ser = serial.Serial(
    PORT,
    BAUD_RATE,
    timeout=1
)

print("Connected to", PORT)
print("Starting data collection...")
print("Press CTRL+C to stop.")
print()


# ==========================================
# CREATE CSV FILE
# ==========================================

file_exists = os.path.isfile(CSV_FILE)

csv_file = open(
    CSV_FILE,
    "a",
    newline="",
    encoding="utf-8"
)

writer = csv.writer(csv_file)

if not file_exists:
    writer.writerow([
        "Timestamp",
        "Raw_ADC",
        "Voltage",
        "Rs_kOhm",
        "Rs_R0",
        "Gas_Index",
        "Delta_Index",
        "Trend"
    ])


# ==========================================
# TEMPORARY STORAGE
# ==========================================

data = {}


# ==========================================
# READ SERIAL DATA
# ==========================================

try:

    while True:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not line:
            continue

        print(line)

        # -------------------------------
        # Extract Raw ADC
        # -------------------------------

        match = re.search(
            r"Raw ADC\s*:\s*([0-9.]+)",
            line
        )

        if match:
            data["Raw_ADC"] = float(match.group(1))


        # -------------------------------
        # Extract Voltage
        # -------------------------------

        match = re.search(
            r"Voltage \(V\)\s*:\s*([0-9.]+)",
            line
        )

        if match:
            data["Voltage"] = float(match.group(1))


        # -------------------------------
        # Extract Rs
        # -------------------------------

        match = re.search(
            r"Rs \(kOhm\)\s*:\s*([0-9.]+)",
            line
        )

        if match:
            data["Rs_kOhm"] = float(match.group(1))


        # -------------------------------
        # Extract Rs/R0
        # -------------------------------

        match = re.search(
            r"Rs/R0\s*:\s*([0-9.]+)",
            line
        )

        if match:
            data["Rs_R0"] = float(match.group(1))


        # -------------------------------
        # Extract Gas Index
        # -------------------------------

        match = re.search(
            r"Gas/VOC Index\s*:\s*(-?[0-9.]+)",
            line
        )

        if match:
            data["Gas_Index"] = float(match.group(1))


        # -------------------------------
        # Extract Delta Index
        # -------------------------------

        match = re.search(
            r"Delta Index\s*:\s*(-?[0-9.]+)",
            line
        )

        if match:
            data["Delta_Index"] = float(match.group(1))


        # -------------------------------
        # Extract Trend
        # -------------------------------

        match = re.search(
            r"Trend\s*:\s*(.*)",
            line
        )

        if match:
            data["Trend"] = match.group(1).strip()


        # =================================
        # WHEN COMPLETE READING IS RECEIVED
        # =================================

        required = [
            "Raw_ADC",
            "Voltage",
            "Rs_kOhm",
            "Rs_R0",
            "Gas_Index",
            "Delta_Index",
            "Trend"
        ]

        if all(key in data for key in required):

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            writer.writerow([
                timestamp,
                data["Raw_ADC"],
                data["Voltage"],
                data["Rs_kOhm"],
                data["Rs_R0"],
                data["Gas_Index"],
                data["Delta_Index"],
                data["Trend"]
            ])

            csv_file.flush()

            print(
                ">>> SAVED:",
                timestamp,
                "Gas Index =",
                data["Gas_Index"]
            )

            # Clear data for next reading
            data = {}


except KeyboardInterrupt:

    print()
    print("Stopping data collection...")


finally:

    csv_file.close()
    ser.close()

    print("CSV file saved as:")
    print(CSV_FILE)