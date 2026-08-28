import pandas as pd

# Load datasets
baseline = pd.read_csv("Baseline_Data.csv")
rose = pd.read_csv("Rose_Experiment_01.csv")

# Add experiment labels
baseline["Experiment"] = "Baseline"
baseline["Flower"] = "None"

rose["Experiment"] = "Rose_01"
rose["Flower"] = "Rose"

# Combine
master = pd.concat(
    [baseline, rose],
    ignore_index=True
)

# Save master dataset
master.to_csv(
    "FreshShield_Master_Dataset.csv",
    index=False
)

print("===================================")
print("FreshShield Master Dataset")
print("===================================")

print("Total readings:", len(master))

print("\nExperiment counts:")
print(master["Experiment"].value_counts())

print("\nGas Index statistics:")
print(master.groupby("Experiment")["Gas_Index"].describe())

print("\nSaved:")
print("FreshShield_Master_Dataset.csv")