import pandas as pd
from pathlib import Path

base = Path(r"C:\Users\jessi\Dissertation")

# CLEANED INPUTS FROM THE UNIFIED CLEANING SCRIPT
rain_path  = base / r"data\climate_yield\cleaned\rain_cru_annual_long.csv"
temp_path  = base / r"data\climate_yield\cleaned\temp_cru_annual_long.csv"
yield_path = base / r"data\climate_yield\cleaned\yield_sugarcane_t_ha_2010_2023.csv"
fert_path  = base / r"data\climate_yield\cleaned\fertilizer_N_kg_ha_2010_2023.csv"
soil_path  = base / r"data\climate_yield\cleaned\soil_index_countries.csv"

out_path   = base / r"data\climate_yield\cleaned\panel_H1_2010_2023.csv"

# 1) Load climate
rain = pd.read_csv(rain_path)   # Year, Country, Rain_mm
temp = pd.read_csv(temp_path)   # Year, Country, Temp_C

climate = rain.merge(temp, on=["Year", "Country"], how="inner")

# 2) Load yield
yield_df = pd.read_csv(yield_path)   # Country, Year, Yield_t_ha

# 3) Load fertilizer
fert_df = pd.read_csv(fert_path)     # Country, Year, Fertilizer_N_kg_ha

# 4) Load soil index
soil_df = pd.read_csv(soil_path)     # Country, SoilIndex

# 5) Merge all
df = (
    climate
    .merge(yield_df, on=["Country", "Year"], how="inner")
    .merge(fert_df, on=["Country", "Year"], how="left")
    .merge(soil_df, on="Country", how="left")
)

# 6) Filter years (safety) and sort
df = df[(df["Year"] >= 2010) & (df["Year"] <= 2023)]
df = df.sort_values(["Country", "Year"])

# 7) Save
out_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_path, index=False)

print("✅ H1 panel saved:", out_path)
print(df.head())
print("\nYears per country:")
print(df.groupby("Country")["Year"].agg(["min", "max"]))
