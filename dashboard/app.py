from flask import Flask, render_template, jsonify
import serial
import threading
import re
import joblib
import pandas as pd
import time
import csv
import os
from datetime import datetime


# ==========================================
# FRESHSHIELD DASHBOARD
# ==========================================

app = Flask(__name__)


# ==========================================
# HC-05
# ==========================================

PORT = "COM4"
BAUD_RATE = 9600


# ==========================================
# ML MODEL
# ==========================================

MODEL_PATH = "../ML/model.pkl"

model = joblib.load(MODEL_PATH)


# ==========================================
# EXPERIMENT CSV
# ==========================================

CSV_FILE = "FreshShield_Experiment_Log.csv"


# ==========================================
# CURRENT EXPERIMENT PHASE
# ==========================================

current_phase = "BASELINE"


# ==========================================
# LATEST DATA
# ==========================================

latest_data = {

    "timestamp": "",

    "phase": "BASELINE",

    "raw": 0,

    "voltage": 0,

    "rs": 0,

    "ratio": 0,

    "gas_index": 0,

    "delta": 0,

    "previous_index": 0,

    "rate_of_change": 0,

    "trend": "WAITING",

    "prediction": 0,

    "bluetooth": "CONNECTING"

}


# ==========================================
# CREATE CSV
# ==========================================

def create_csv():

    if not os.path.exists(CSV_FILE):

        with open(
            CSV_FILE,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "Timestamp",
                "Phase",
                "Raw_ADC",
                "Voltage",
                "Rs_kOhm",
                "Rs_R0",
                "Gas_Index",
                "Delta_Index",
                "Previous_Gas_Index",
                "Rate_of_Change",
                "Trend",
                "ML_Prototype_ppm"

            ])


# ==========================================
# SAVE READING
# ==========================================

def save_reading(data):

    with open(
        CSV_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            data["timestamp"],

            data["phase"],

            data["raw"],

            data["voltage"],

            data["rs"],

            data["ratio"],

            data["gas_index"],

            data["delta"],

            data["previous_index"],

            data["rate_of_change"],

            data["trend"],

            data["prediction"]

        ])


# ==========================================
# BLUETOOTH READER
# ==========================================

def bluetooth_reader():

    global latest_data

    try:

        ser = serial.Serial(
            PORT,
            BAUD_RATE,
            timeout=2
        )

        time.sleep(2)

        latest_data["bluetooth"] = "CONNECTED"

        print(
            "HC-05 connected on",
            PORT
        )

        while True:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()


            if not line:
                continue


            print(
                "DATA:",
                line
            )


            # ==================================
            # EXTRACT VALUES
            # ==================================

            raw = re.search(
                r"RAW=([-0-9.]+)",
                line
            )

            voltage = re.search(
                r"V=([-0-9.]+)",
                line
            )

            rs = re.search(
                r"RS=([-0-9.]+)",
                line
            )

            ratio = re.search(
                r"RATIO=([-0-9.]+)",
                line
            )

            gi = re.search(
                r"GI=([-0-9.]+)",
                line
            )

            delta = re.search(
                r"DELTA=([-0-9.]+)",
                line
            )

            trend = re.search(
                r"TREND=([A-Za-z]+)",
                line
            )


            # ==================================
            # UPDATE SENSOR VALUES
            # ==================================

            if raw:
                latest_data["raw"] = float(
                    raw.group(1)
                )

            if voltage:
                latest_data["voltage"] = float(
                    voltage.group(1)
                )

            if rs:
                latest_data["rs"] = float(
                    rs.group(1)
                )

            if ratio:
                latest_data["ratio"] = float(
                    ratio.group(1)
                )

            if gi:
                latest_data["gas_index"] = float(
                    gi.group(1)
                )

            if delta:
                latest_data["delta"] = float(
                    delta.group(1)
                )

            if trend:
                latest_data["trend"] = (
                    trend.group(1)
                )


            # ==================================
            # PREVIOUS INDEX
            # ==================================

            gas_index = latest_data[
                "gas_index"
            ]

            delta_index = latest_data[
                "delta"
            ]

            previous_index = (
                gas_index - delta_index
            )

            latest_data[
                "previous_index"
            ] = previous_index


            # ==================================
            # RATE OF CHANGE
            # ==================================

            rate_of_change = delta_index

            latest_data[
                "rate_of_change"
            ] = rate_of_change


            # ==================================
            # ML PREDICTION
            # ==================================

            input_data = pd.DataFrame([{

                "Gas_Index":
                    gas_index,

                "Previous_Gas_Index":
                    previous_index,

                "Delta_Gas_Index":
                    delta_index,

                "Rate_of_Change":
                    rate_of_change

            }])


            prediction = model.predict(
                input_data
            )[0]


            latest_data[
                "prediction"
            ] = round(
                float(prediction),
                4
            )


            # ==================================
            # TIMESTAMP + PHASE
            # ==================================

            latest_data[
                "timestamp"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            latest_data[
                "phase"
            ] = current_phase


            # ==================================
            # SAVE
            # ==================================

            save_reading(
                latest_data
            )


    except Exception as e:

        latest_data[
            "bluetooth"
        ] = "ERROR"

        print(
            "Bluetooth error:",
            e
        )


# ==========================================
# HOME
# ==========================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==========================================
# SENSOR API
# ==========================================

@app.route("/api/data")
def api_data():

    return jsonify(
        latest_data
    )


# ==========================================
# CHANGE EXPERIMENT PHASE
# ==========================================

@app.route(
    "/api/phase/<phase>",
    methods=["GET"]
)
def change_phase(phase):

    global current_phase

    allowed_phases = [

        "BASELINE",
        "ROSE_EXPOSURE",
        "TREATMENT",
        "RECOVERY"

    ]

    phase = phase.upper()

    if phase not in allowed_phases:

        return jsonify({

            "success": False,

            "message": "Invalid phase"

        }), 400


    current_phase = phase

    latest_data[
        "phase"
    ] = phase


    print(
        "EXPERIMENT PHASE:",
        phase
    )


    return jsonify({

        "success": True,

        "phase": phase

    })


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    create_csv()


    bluetooth_thread = threading.Thread(
        target=bluetooth_reader,
        daemon=True
    )


    bluetooth_thread.start()


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )