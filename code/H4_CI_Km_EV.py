import pandas as pd

# ========= 1. LOAD DATA =========
path_ethanol_scen = r"C:\Users\jessi\Dissertation\data\processed\H4_ethanol_CI_scenarios.csv"
path_grid_filt    = r"C:\Users\jessi\Dissertation\data\processed\H4_EU_grid_CI_filtered.csv"
path_grid_proc    = r"C:\Users\jessi\Dissertation\data\processed\H4_EU_grid_CI_processed.csv"
path_bev_cons     = r"C:\Users\jessi\Dissertation\data\processed\H4_BEV_energy_consumption.csv"
path_bev_life     = r"C:\Users\jessi\Dissertation\data\processed\H4_BEV_lifetime_km.csv"
path_ethanol_base = r"C:\Users\jessi\Dissertation\data\processed\H4_ethanol_CI_baseline.csv"

df_grid = pd.read_csv(path_grid_proc)      # expects: country, CI_gCO2_per_kWh_2022_2024_avg
df_cons = pd.read_csv(path_bev_cons)       # expects: consumption_kWh_per_km column
df_life = pd.read_csv(path_bev_life)       # expects: lifetime_km column

# ========= 2. SET BATTERY PARAMETERS (IVL mid-case) =========
BATTERY_GWP_KG_PER_KWH = 77      # kg CO2e / kWh battery (IVL mid)
BATTERY_CAPACITY_KWH   = 60      # kWh (choose your representative BEV)
lifetime_km            = df_life["lifetime_km"].iloc[0]

# total embedded battery emissions over life (g CO2e)
E_bat_total_g = BATTERY_GWP_KG_PER_KWH * BATTERY_CAPACITY_KWH * 1000
E_bat_per_km_g = E_bat_total_g / lifetime_km

# ========= 3. OPERATIONAL EMISSIONS PER KM =========
# use first (or chosen) BEV fleet-average value
cons_kWh_per_km = df_cons["consumption_kWh_per_km"].iloc[0]

df_grid["CI_EV_operational_gCO2_per_km"] = (
    df_grid["CI_gCO2_per_kWh_2022_2024_avg"] * cons_kWh_per_km
)

# ========= 4. TOTAL EV CI PER KM (OPERATIONAL + BATTERY) =========
df_grid["CI_EV_battery_gCO2_per_km"] = E_bat_per_km_g
df_grid["CI_EV_total_gCO2_per_km"] = (
    df_grid["CI_EV_operational_gCO2_per_km"] + df_grid["CI_EV_battery_gCO2_per_km"]
)

# ========= 5. SAVE RESULT =========
out_path = r"C:\Users\jessi\Dissertation\data\processed\H4_EV_CI_per_km.csv"
df_grid.to_csv(out_path, index=False)

print("Saved:", out_path)
