import pandas as pd
import matplotlib.pyplot as plt
import os

# === INPUT / OUTPUT PATHS ===
path_ev  = r"C:\Users\jessi\Dissertation\data\processed\H4_EV_CI_per_km.csv"
fig_dir  = r"C:\Users\jessi\Dissertation\figures"
fig_path = os.path.join(fig_dir, "H4_Fig_X2_BEV_CI.png")

os.makedirs(fig_dir, exist_ok=True)

# === LOAD DATA ===
df_ev = pd.read_csv(path_ev)

# Ensure expected columns exist
required_cols = [
    "Countries",
    "CI_EV_operational_gCO2_per_km",
    "CI_EV_battery_gCO2_per_km",
    "CI_EV_total_gCO2_per_km",
]
missing = [c for c in required_cols if c not in df_ev.columns]
if missing:
    raise ValueError(f"Missing columns in H4_EV_CI_per_km.csv: {missing}")

countries   = df_ev["Countries"]
operational = df_ev["CI_EV_operational_gCO2_per_km"]
battery     = df_ev["CI_EV_battery_gCO2_per_km"]

# === PLOT STACKED BARS ===
plt.figure(figsize=(8, 5))

plt.bar(countries, operational, label="Operational")
plt.bar(countries, battery, bottom=operational, label="Battery (embedded)")

plt.xlabel("Electricity system")
plt.ylabel("BEV carbon intensity (gCO₂e/km)")
plt.title("Figure H4.X.2. BEV carbon intensity per kilometre\n(operational and embedded components)")

plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.savefig(fig_path, dpi=300)
plt.close()

print(f"Saved: {fig_path}")
