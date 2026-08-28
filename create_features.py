import pandas as pd
import numpy as np

# ==========================================
# FRESHSHIELD - CREATE ML FEATURES
# ==========================================

print("===================================")
print(" FreshShield ML Feature Generator")
print("===================================")

# ==========================================
# LOAD DATA
# ==========================================

baseline = pd.read_csv("Baseline_Data.csv")
rose = pd.read_csv("Rose_Experiment_01.csv")

print("\nBaseline readings:", len(baseline))
print("Rose readings    :", len(rose))

# ==========================================
# LABEL EXPERIMENTS
# ==========================================

baseline["Experiment"] = "Baseline"
rose["Experiment"] = "Rose_01"

baseline["Flower"] = "None"
rose["Flower"] = "Rose"

# ==========================================
# COMBINE DATA
# ==========================================

df = pd.concat(
    [baseline, rose],
    ignore_index=True
)

# ==========================================
# CONVERT TIMESTAMP
# ==========================================

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

# Remove rows with invalid timestamps

df = df.dropna(
    subset=["Timestamp"]
)

# Sort by time

df = df.sort_values(
    "Timestamp"
).reset_index(
    drop=True
)

# ==========================================
# CONVERT GAS INDEX TO NUMBER
# ==========================================

df["Gas_Index"] = pd.to_numeric(
    df["Gas_Index"],
    errors="coerce"
)

# ==========================================
# PREVIOUS GAS INDEX
# ==========================================

df["Previous_Gas_Index"] = (
    df["Gas_Index"].shift(1)
)

# ==========================================
# DELTA GAS INDEX
# ==========================================

df["Delta_Gas_Index"] = (
    df["Gas_Index"]
    -
    df["Previous_Gas_Index"]
)

# ==========================================
# TIME DIFFERENCE
# ==========================================

df["Time_Difference"] = (
    df["Timestamp"]
    .diff()
    .dt.total_seconds()
)

# ==========================================
# SAFE RATE OF CHANGE
# ==========================================

df["Rate_of_Change"] = 0.0

valid_time = (
    df["Time_Difference"] > 0
)

df.loc[
    valid_time,
    "Rate_of_Change"
] = (
    df.loc[
        valid_time,
        "Delta_Gas_Index"
    ]
    /
    df.loc[
        valid_time,
        "Time_Difference"
    ]
)

# ==========================================
# NUMERIC COLUMNS
# ==========================================

numeric_columns = [
    "Raw_ADC",
    "Voltage",
    "Rs_kOhm",
    "Rs_R0",
    "Gas_Index",
    "Delta_Index",
    "Previous_Gas_Index",
    "Delta_Gas_Index",
    "Time_Difference",
    "Rate_of_Change"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# ==========================================
# REMOVE INFINITY
# ==========================================

df.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

# ==========================================
# REMOVE INVALID ML ROWS
# ==========================================

required_columns = [
    "Gas_Index",
    "Previous_Gas_Index",
    "Delta_Gas_Index",
    "Rate_of_Change"
]

df = df.dropna(
    subset=required_columns
).reset_index(
    drop=True
)

# ==========================================
# FINAL INFINITY CHECK
# ==========================================

infinity_count = 0

for column in required_columns:

    infinity_count += np.isinf(
        df[column].to_numpy()
    ).sum()

# ==========================================
# SAVE ML DATASET
# ==========================================

output_file = "FreshShield_ML_Dataset.csv"

df.to_csv(
    output_file,
    index=False
)

# ==========================================
# REPORT
# ==========================================

print("\n===================================")
print(" FRESHSHIELD ML DATASET")
print("===================================")

print(
    "\nTotal ML readings:",
    len(df)
)

print(
    "\nColumns:"
)

print(
    df.columns.tolist()
)

print(
    "\n-----------------------------------"
)

print(
    "RATE OF CHANGE"
)

print(
    df["Rate_of_Change"].describe()
)

print(
    "\n-----------------------------------"
)

print(
    "INFINITY VALUES:",
    infinity_count
)

print(
    "\n-----------------------------------"
)

print(
    "GAS INDEX"
)

print(
    df["Gas_Index"].describe()
)

print(
    "\n-----------------------------------"
)

print(
    "EXPERIMENTS"
)

print(
    df["Experiment"].value_counts()
)

print(
    "\n-----------------------------------"
)

print(
    "Saved as:"
)

print(
    output_file
)

print(
    "\n==================================="
)

print(
    " FEATURE GENERATION COMPLETE"
)

print(
    "==================================="
)