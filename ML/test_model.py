import joblib
import pandas as pd

model = joblib.load("model.pkl")

print("===================================")
print(" FRESHSHIELD MODEL TEST")
print("===================================")

test_values = [
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    20,
    23
]

print()
print("Gas Index -> Predicted ppm")
print("-----------------------------------")

for gas_index in test_values:

    data = pd.DataFrame([{
        "Gas_Index": gas_index,
        "Previous_Gas_Index": gas_index,
        "Delta_Gas_Index": 0,
        "Rate_of_Change": 0
    }])

    prediction = model.predict(data)[0]

    print(
        f"{gas_index:8.2f} -> {prediction:.6f} ppm"
    )

print("-----------------------------------")