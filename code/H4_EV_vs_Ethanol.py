import pandas as pd

# ===== Paths =====
path_ev   = r"C:\Users\jessi\Dissertation\data\processed\H4_EV_CI_per_km.csv"
path_eth  = r"C:\Users\jessi\Dissertation\data\processed\H4_ethanol_CI_per_km_baseline.csv"
out_path  = r"C:\Users\jessi\Dissertation\data\processed\H4_EV_vs_ethanol_comparison.csv"

# ===== Load data =====
df_ev = pd.read_csv(path_ev)          # expects: Countries, CI_EV_total_gCO2_per_km, ...
df_eth = pd.read_csv(path_eth)        # country, CI_ethanol_gCO2e_km

# Get ethanol values as a dict
eth_dict = dict(zip(df_eth["country"], df_eth["CI_ethanol_gCO2e_km"]))

# ===== Build wide comparison table =====
df_comp = df_ev[["Countries", "CI_EV_total_gCO2_per_km"]].copy()

df_comp["CI_ethanol_Mozambique_gCO2e_km"]   = eth_dict.get("Mozambique")
df_comp["CI_ethanol_SouthAfrica_gCO2e_km"]  = eth_dict.get("South Africa")
df_comp["CI_ethanol_Kenya_gCO2e_km"]        = eth_dict.get("Kenya")
df_comp["CI_ethanol_Brazil_gCO2e_km"]       = eth_dict.get("Brazil")

# Optional: round
df_comp = df_comp.round(2)

# Save
df_comp.to_csv(out_path, index=False)
print("Saved:", out_path)
