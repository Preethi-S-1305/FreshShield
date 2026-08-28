import pandas as pd

df = pd.read_csv("../FreshShield_ML_Dataset.csv")

print("===================================")
print(" FRESHSHIELD ML DATASET INSPECTION")
print("===================================")

print("\nTOTAL ROWS:")
print(len(df))

print("\nCOLUMNS:")
print(df.columns.tolist())

print("\n-----------------------------------")
print("FEATURE RANGES")
print("-----------------------------------")

features = [
    "Gas_Index",
    "Previous_Gas_Index",
    "Delta_Gas_Index",
    "Rate_of_Change"
]

for col in features:

    print(
        f"{col:22s}: "
        f"min={df[col].min():.4f}, "
        f"max={df[col].max():.4f}, "
        f"mean={df[col].mean():.4f}"
    )


print("\n-----------------------------------")
print("TARGET COLUMNS")
print("-----------------------------------")

for col in df.columns:

    if (
        "ppm" in col.lower()
        or "ethylene" in col.lower()
        or "target" in col.lower()
    ):

        print("\nTARGET:", col)

        print(
            df[col].describe()
        )

        print(
            "Unique values:",
            df[col].nunique()
        )


print("\n-----------------------------------")
print("EXPERIMENTS")
print("-----------------------------------")

if "Experiment" in df.columns:

    print(
        df["Experiment"].value_counts()
    )


print("\n-----------------------------------")
print("FLOWER")
print("-----------------------------------")

if "Flower" in df.columns:

    print(
        df["Flower"].value_counts(
            dropna=False
        )
    )


print("\n===================================")