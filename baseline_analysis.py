import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("FreshShield_Data.csv")

plt.figure(figsize=(10, 5))

plt.plot(df["Gas_Index"])

plt.xlabel("Reading Number")
plt.ylabel("Gas/VOC Index")
plt.title("FreshShield Baseline Gas/VOC Index")

plt.grid(True)

plt.savefig("FreshShield_Baseline.png", dpi=300)

plt.show()