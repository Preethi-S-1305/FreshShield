import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# ==========================================
# FRESHSHIELD ML MODEL
# ==========================================

print("===================================")
print(" FRESHSHIELD ML MODEL")
print("===================================")


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "../FreshShield_ML_Dataset.csv"
)

print(
    "\nOriginal readings:",
    len(df)
)


# ==========================================
# FEATURES
# ==========================================

features = [
    "Gas_Index",
    "Previous_Gas_Index",
    "Delta_Gas_Index",
    "Rate_of_Change"
]


# ==========================================
# CONVERT FEATURES TO NUMERIC
# ==========================================

for column in features:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ==========================================
# REMOVE INFINITY
# ==========================================

df[features] = df[features].replace(
    [np.inf, -np.inf],
    np.nan
)


# ==========================================
# REMOVE INVALID ROWS
# ==========================================

df = df.dropna(
    subset=features
).reset_index(
    drop=True
)


print(
    "Clean readings:",
    len(df)
)


# ==========================================
# PROTOTYPE TARGET
# ==========================================

# IMPORTANT:
#
# This is NOT a measured ethylene
# concentration.
#
# It is a temporary mathematical
# prototype target used to demonstrate
# the complete ML pipeline.
#
# Formula:
#
# Prototype Estimate = Gas Index × 0.03
#
# This must NOT be presented as a
# calibrated MQ-125 ethylene measurement.

df["Ethylene_Prototype"] = (
    df["Gas_Index"] * 0.03
)


# ==========================================
# INPUT DATA
# ==========================================

X = df[features]

y = df[
    "Ethylene_Prototype"
]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ==========================================
# RANDOM FOREST MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    min_samples_leaf=2,
    n_jobs=-1
)


# ==========================================
# TRAIN
# ==========================================

model.fit(
    X_train,
    y_train
)


# ==========================================
# TEST
# ==========================================

predictions = model.predict(
    X_test
)


# ==========================================
# EVALUATION
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


# ==========================================
# RESULTS
# ==========================================

print(
    "\n==================================="
)

print(
    "TRAINING RESULTS"
)

print(
    "==================================="
)

print(
    "Training readings:",
    len(X_train)
)

print(
    "Testing readings :",
    len(X_test)
)

print(
    "\nMAE:",
    round(mae, 6)
)

print(
    "R² :",
    round(r2, 6)
)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

print(
    "\n==================================="
)

print(
    "FEATURE IMPORTANCE"
)

print(
    "==================================="
)

importance = pd.DataFrame({

    "Feature": features,

    "Importance":
        model.feature_importances_

})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print(
    importance.to_string(
        index=False
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

model_file = "model.pkl"

joblib.dump(
    model,
    model_file
)


# ==========================================
# SAVE MODEL INFORMATION
# ==========================================

model_info = {

    "model_type":
        "RandomForestRegressor",

    "features":
        features,

    "target":
        "Ethylene_Prototype",

    "target_formula":
        "Gas_Index * 0.03",

    "training_readings":
        len(X_train),

    "testing_readings":
        len(X_test),

    "MAE":
        float(mae),

    "R2":
        float(r2)

}

joblib.dump(
    model_info,
    "model_info.pkl"
)


# ==========================================
# FINISHED
# ==========================================

print(
    "\n==================================="
)

print(
    "MODEL SAVED"
)

print(
    "==================================="
)

print(
    "Model:",
    "D:\\FreshShield\\ML\\model.pkl"
)

print(
    "Info :",
    "D:\\FreshShield\\ML\\model_info.pkl"
)

print(
    "\nPrototype target reminder:"
)

print(
    "This is NOT calibrated ethylene ppm."
)

print(
    "==================================="
)