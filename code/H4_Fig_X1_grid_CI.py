import pandas as pd
import matplotlib.pyplot as plt

# === INPUT / OUTPUT PATHS ===
path_grid = r"C:\Users\jessi\Dissertation\data\processed\H4_EU_grid_CI_processed.csv"
fig_path  = r"C:\Users\jessi\Dissertation\figures\H4_Fig_X1_grid_CI.png"

# === LOAD DATA ===
df_grid = pd.read_csv(path_grid)

# FIX: Your column is named "Countries", not "country"
countries = df_grid["Countries"]
ci_values = df_grid["CI_gCO2_per_kWh_2022_2024_avg"]

# Optional sort
df_grid = df_grid.sort_values("CI_gCO2_per_kWh_2022_2024_avg")
countries = df_grid["Countries"]
ci_values = df_grid["CI_gCO2_per_kWh_2022_2024_avg"]

# === PLOT ===
plt.figure(figsize=(8, 5))
plt.bar(countries, ci_values)

plt.xlabel("Electricity system")
plt.ylabel("Grid carbon intensity (gCO₂e/kWh)")
plt.title("Figure H4.X.1. Average electricity-grid carbon intensity, 2022–2024")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(fig_path, dpi=300)
plt.close()

print(f"Saved: {fig_path}")
