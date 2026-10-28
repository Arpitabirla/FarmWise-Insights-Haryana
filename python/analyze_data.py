from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "haryana_crop_demo_data.csv"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
print("DEMO DATA ONLY — do not report these numbers as official Haryana statistics.")
print("\nShape:", df.shape)
print("\nMissing values:\n", df.isna().sum())
print("\nTotal production by crop (tonnes):\n",
      df.groupby("Crop")["Production_Tonnes"].sum().sort_values(ascending=False).round(1))
print("\nAverage yield by crop:\n",
      df.groupby("Crop")["Yield_Tonnes_Per_Hectare"].mean().sort_values(ascending=False).round(2))
print("\nProduction by district (tonnes):\n",
      df.groupby("District")["Production_Tonnes"].sum().sort_values(ascending=False).round(1))

yearly = df.groupby(["Year","Crop"], as_index=False)["Production_Tonnes"].sum()
pivot = yearly.pivot(index="Year", columns="Crop", values="Production_Tonnes")
ax = pivot.plot(kind="line", marker="o", figsize=(10,6), title="Crop Production Trend (Illustrative Demo Data)")
ax.set_ylabel("Production (tonnes)")
ax.set_xlabel("Year")
plt.tight_layout()
plt.savefig(OUT / "production_trend.png", dpi=160)
print(f"\nSaved chart: {OUT / 'production_trend.png'}")
