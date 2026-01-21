import pandas as pd

# ====== 1. PATHS ======
path_ethanol_base = r"C:\Users\jessi\Dissertation\data\processed\H4_ethanol_CI_baseline.csv"
path_ethanol_scen = r"C:\Users\jessi\Dissertation\data\processed\H4_ethanol_CI_scenarios.csv"

# ====== 2. LOAD DATA ======
df_ethanol_base = pd.read_csv(path_ethanol_base)   # columns: country, CI_ethanol_gCO2e_MJ
df_ethanol_scen = pd.read_csv(path_ethanol_scen)   # columns: scenario, CI_ethanol_gCO2e_MJ

# ====== 3. CONSTANT: ENERGY USE PER KM ======
MJ_PER_KM = 2.2   # ethanol vehicle energy consumption (MJ/km)

# ====== 4. CALCULATE gCO2e PER KM ======
df_ethanol_base["CI_ethanol_gCO2e_km"] = (
    df_ethanol_base["CI_ethanol_gCO2e_MJ"] * MJ_PER_KM
)

df_ethanol_scen["CI_ethanol_gCO2e_km"] = (
    df_ethanol_scen["CI_ethanol_gCO2e_MJ"] * MJ_PER_KM
)

# ====== 5. SAVE OUTPUTS ======
out_base = r"C:\Users\jessi\Dissertation\data\processed\H4_ethanol_CI_per_km_baseline.csv"
out_scen = r"C:\Users\jessi\Dissertation\data\processed\H4_ethanol_CI_per_km_scenarios.csv"

df_ethanol_base.to_csv(out_base, index=False)
df_ethanol_scen.to_csv(out_scen, index=False)

print("Saved baseline:", out_base)
print("Saved scenarios:", out_scen)
