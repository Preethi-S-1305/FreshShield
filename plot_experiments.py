import pandas as pd
import matplotlib.pyplot as plt

# Load ML dataset
df = pd.read_csv("FreshShield_ML_Dataset.csv")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Plot Gas Index
plt.figure(figsize=(12, 6))

for experiment in df["Experiment"].unique():

    data = df[df["Experiment"] == experiment]

    plt.plot(
        data["Timestamp"],
        data["Gas_Index"],
        label=experiment
    )

plt.xlabel("Time")
plt.ylabel("Gas/VOC Index")
plt.title("FreshShield - Gas/VOC Response")

plt.legend()
plt.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "FreshShield_Experiment_Comparison.png",
    dpi=300
)

plt.show()