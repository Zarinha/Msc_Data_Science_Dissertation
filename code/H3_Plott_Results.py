import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Paths
# ---------------------------------------------------------
DATA_DIR = r"C:\Users\jessi\Dissertation\data\processed"
FIG_DIR = r"C:\Users\jessi\Dissertation\figures"

RESULT_FILE = "H3_CI_GHG_Results.csv"

os.makedirs(FIG_DIR, exist_ok=True)

# ---------------------------------------------------------
# 2. Load results
# ---------------------------------------------------------
results_path = os.path.join(DATA_DIR, RESULT_FILE)
df = pd.read_csv(results_path)

df["Label"] = df["Exporting_Country"]

# ---------------------------------------------------------
# 3. Figure 1 – Carbon intensity comparison
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
x = range(len(df))

plt.bar(x, df["CI_ethanol_gCO2e_MJ"])
plt.xticks(x, df["Label"], rotation=0)
plt.ylabel("Carbon intensity of ethanol (gCO₂e/MJ)")
plt.title("H3 – Carbon intensity of sugarcane ethanol exported to Europe")

for i, v in enumerate(df["CI_ethanol_gCO2e_MJ"]):
    plt.text(i, v + 0.3, f"{v:.1f}", ha="center", fontsize=9)

plt.tight_layout()

f1 = os.path.join(FIG_DIR, "H3_Carbon_Intensity_Comparison.png")
plt.savefig(f1, dpi=300)
plt.close()
print(f"Saved: {f1}")

# ---------------------------------------------------------
# 4. Figure 2 – GHG reduction comparison
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))

plt.bar(x, df["GHG_reduction_percent"])
plt.xticks(x, df["Label"])
plt.ylabel("GHG reduction (%)")
plt.title("H3 – GHG reduction relative to EU gasoline baseline")

# RED II threshold line
REDII = 65
plt.axhline(REDII, ls="--", color="black")
plt.text(len(df)-0.1, REDII + 1, "RED II threshold (65%)", ha="right", fontsize=9)

for i, v in enumerate(df["GHG_reduction_percent"]):
    plt.text(i, v + 0.7, f"{v:.1f}%", ha="center", fontsize=9)

plt.ylim(0, max(df["GHG_reduction_percent"]) * 1.2)
plt.tight_layout()

f2 = os.path.join(FIG_DIR, "H3_GHG_Reduction_Comparison.png")
plt.savefig(f2, dpi=300)
plt.close()
print(f"Saved: {f2}")
