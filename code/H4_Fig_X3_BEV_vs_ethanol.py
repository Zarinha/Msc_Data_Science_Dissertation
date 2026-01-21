import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# === INPUT / OUTPUT PATHS ===
path_comp = r"C:\Users\jessi\Dissertation\data\processed\H4_EV_vs_ethanol_comparison.csv"
fig_dir   = r"C:\Users\jessi\Dissertation\figures"
fig_path  = os.path.join(fig_dir, "H4_Fig_X3_BEV_vs_ethanol.png")

os.makedirs(fig_dir, exist_ok=True)

# === LOAD DATA ===
df_comp = pd.read_csv(path_comp)

required_cols = [
    "Countries",
    "CI_EV_total_gCO2_per_km",
    "CI_ethanol_Mozambique_gCO2e_km",
    "CI_ethanol_SouthAfrica_gCO2e_km",
    "CI_ethanol_Kenya_gCO2e_km",
    "CI_ethanol_Brazil_gCO2e_km",
]
missing = [c for c in required_cols if c not in df_comp.columns]
if missing:
    raise ValueError(f"Missing columns in H4_EV_vs_ethanol_comparison.csv: {missing}")

countries = df_comp["Countries"]
bev       = df_comp["CI_EV_total_gCO2_per_km"]
eth_moz   = df_comp["CI_ethanol_Mozambique_gCO2e_km"]
eth_sa    = df_comp["CI_ethanol_SouthAfrica_gCO2e_km"]
eth_ken   = df_comp["CI_ethanol_Kenya_gCO2e_km"]
eth_br    = df_comp["CI_ethanol_Brazil_gCO2e_km"]

x = np.arange(len(countries))
bar_width = 0.15

plt.figure(figsize=(10, 5))

plt.bar(x - 2*bar_width, bev,    width=bar_width, label="BEV")
plt.bar(x - 1*bar_width, eth_moz, width=bar_width, label="Ethanol – Mozambique")
plt.bar(x,                eth_sa,  width=bar_width, label="Ethanol – South Africa")
plt.bar(x + 1*bar_width, eth_ken,  width=bar_width, label="Ethanol – Kenya")
plt.bar(x + 2*bar_width, eth_br,   width=bar_width, label="Ethanol – Brazil")

plt.xlabel("Electricity system")
plt.ylabel("Carbon intensity (gCO₂e/km)")
plt.title("Figure H4.X.3. Comparison of BEV and ethanol pathways by electricity system")

plt.xticks(x, countries, rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.savefig(fig_path, dpi=300)
plt.close()

print(f"Saved: {fig_path}")
