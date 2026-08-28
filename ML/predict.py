import serial
import joblib
import pandas as pd
import re
import time

# ==========================================
# FRESHSHIELD
# HC-05 BLUETOOTH + ML
# ==========================================

PORT = "COM4"
BAUD_RATE = 9600

# Load trained model
model = joblib.load("model.pkl")

print("===================================")
print(" FRESHSHIELD WIRELESS ML SYSTEM")
print("===================================")
print("Connecting to HC-05 on", PORT)

ser = serial.Serial(
    PORT,
    BAUD_RATE,
    timeout=2
)

time.sleep(2)

print("HC-05 connected!")
print("Waiting for Arduino data...")
print("-----------------------------------")


while True:

    try:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not line:
            continue

        print("DATA:", line)

        # =================================
        # Parse Arduino compact format
        # =================================

        raw_match = re.search(
            r"RAW=([-0-9.]+)",
            line
        )

        voltage_match = re.search(
            r"V=([-0-9.]+)",
            line
        )

        rs_match = re.search(
            r"RS=([-0-9.]+)",
            line
        )

        ratio_match = re.search(
            r"RATIO=([-0-9.]+)",
            line
        )

        gi_match = re.search(
            r"GI=([-0-9.]+)",
            line
        )

        delta_match = re.search(
            r"DELTA=([-0-9.]+)",
            line
        )

        trend_match = re.search(
            r"TREND=([A-Za-z]+)",
            line
        )


        # =================================
        # Make sure required values exist
        # =================================

        if gi_match and delta_match:

            gas_index = float(
                gi_match.group(1)
            )

            delta_index = float(
                delta_match.group(1)
            )

            # Your Arduino sends approximately
            # one reading every second.
            rate_of_change = delta_index


            # Previous Gas Index
            previous_index = (
                gas_index - delta_index
            )


            # =================================
            # ML INPUT
            # =================================

            input_data = pd.DataFrame([{
                "Gas_Index": gas_index,

                "Previous_Gas_Index":
                    previous_index,

                "Delta_Gas_Index":
                    delta_index,

                "Rate_of_Change":
                    rate_of_change
            }])


            # =================================
            # ML PREDICTION
            # =================================

            prediction = model.predict(
                input_data
            )[0]


            # =================================
            # DISPLAY
            # =================================

            print()
            print("===================================")
            print("       FRESHSHIELD LIVE")
            print("===================================")

            print(
                "Gas/VOC Index      :",
                gas_index
            )

            print(
                "Delta Index        :",
                delta_index
            )

            print(
                "Previous Index     :",
                round(previous_index, 2)
            )

            print(
                "Rate of Change     :",
                round(rate_of_change, 3)
            )

            print(
                "ML Prototype ppm   :",
                round(prediction, 4)
            )

            if trend_match:

                trend = trend_match.group(1)

                print(
                    "Trend              :",
                    trend
                )

            print("===================================")


    except KeyboardInterrupt:

        print("\nStopping FreshShield...")
        break

    except Exception as e:

        print("Error:", e)


ser.close()