import pandas as pd
from pathlib import Path

# ============================
# CONFIG
# ============================
base = Path(r"C:\Users\jessi\Dissertation")

# RAW INPUTS
rain_wide_path = base / r"data\processed\precip_cru_annual_MOZ_ZAF_KEN_BRA.csv"
temp_wide_path = base / r"data\climate_yield\cleaned\cru_annual_temp_countries.csv"
yield_raw_path = base / r"data\raw\FAO_sugarcane_yield_2010_2023.csv"
fert_raw_path  = base / r"data\raw\FAOSTAT_Nitrogen_11-9-2025.csv"

# CLEANED OUTPUT FOLDER
clean_dir = base / r"data\climate_yield\cleaned"
clean_dir.mkdir(parents=True, exist_ok=True)

rain_long_out  = clean_dir / "rain_cru_annual_long.csv"
temp_long_out  = clean_dir / "temp_cru_annual_long.csv"
yield_out      = clean_dir / "yield_sugarcane_t_ha_2010_2023.csv"
fert_out       = clean_dir / "fertilizer_N_kg_ha_2010_2023.csv"
soil_out       = clean_dir / "soil_index_countries.csv"

countries_keep = ["Mozambique", "South Africa", "Kenya", "Brazil"]

# ============================
# 1) RAINFALL: wide → long
# ============================
print("=== RAINFALL (CRU) ===")
rain = pd.read_csv(rain_wide_path)
print("Columns:", rain.columns.tolist())

# Expect first column Year, rest = countries
if "Year" not in rain.columns:
    raise ValueError("Rain file must have 'Year' column")

value_cols = [c for c in rain.columns if c != "Year"]
rain_long = rain.melt(id_vars="Year", value_vars=value_cols,
                      var_name="Country", value_name="Rain_mm")
rain_long = rain_long[rain_long["Country"].isin(countries_keep)]
rain_long.to_csv(rain_long_out, index=False)

print("Saved:", rain_long_out)
print(rain_long.head())

# ============================
# 2) TEMPERATURE: wide → long
# ============================
print("\n=== TEMPERATURE (CRU) ===")
temp = pd.read_csv(temp_wide_path)
print("Columns:", temp.columns.tolist())

if "Year" not in temp.columns:
    raise ValueError("Temp file must have 'Year' column")

value_cols = [c for c in temp.columns if c != "Year"]
temp_long = temp.melt(id_vars="Year", value_vars=value_cols,
                      var_name="Country", value_name="Temp_C")
temp_long = temp_long[temp_long["Country"].isin(countries_keep)]
temp_long.to_csv(temp_long_out, index=False)

print("Saved:", temp_long_out)
print(temp_long.head())

# ============================
# 3) YIELD: FAO hg/ha → t/ha
# ============================
print("\n=== YIELD (FAO) ===")
yd_raw = pd.read_csv(yield_raw_path)
print("Columns:", yd_raw.columns.tolist())

# AREA → COUNTRY if needed
if "Area" in yd_raw.columns and "Country" not in yd_raw.columns:
    yd_raw = yd_raw.rename(columns={"Area": "Country"})

# Filter sugarcane + yield if present
if "Item" in yd_raw.columns:
    yd_raw = yd_raw[yd_raw["Item"].str.contains("Sugar cane", case=False, na=False)]
if "Element" in yd_raw.columns:
    yd_raw = yd_raw[yd_raw["Element"].str.contains("Yield", case=False, na=False)]

if "Value" not in yd_raw.columns:
    raise ValueError("Yield file must have 'Value' column")

yd_raw = yd_raw.rename(columns={"Value": "Yield_hg_ha"})
yd_raw["Year"] = yd_raw["Year"].astype(int)
yd_raw["Yield_t_ha"] = yd_raw["Yield_hg_ha"] * 0.0001  # hg/ha → t/ha

yd_clean = yd_raw[["Country", "Year", "Yield_t_ha"]].dropna()
yd_clean = yd_clean[yd_clean["Country"].isin(countries_keep)]
yd_clean = yd_clean[(yd_clean["Year"] >= 2010) & (yd_clean["Year"] <= 2023)]

yd_clean.to_csv(yield_out, index=False)

print("Saved:", yield_out)
print(yd_clean.head())
print("Yield countries:", yd_clean["Country"].unique())

# ============================
# 4) FERTILIZER: FAO RFN kg/ha
# ============================
print("\n=== FERTILIZER N (FAO RFN) ===")
ft_raw = pd.read_csv(fert_raw_path)
print("Columns:", ft_raw.columns.tolist())

# AREA → COUNTRY if needed
if "Area" in ft_raw.columns and "Country" not in ft_raw.columns:
    ft_raw = ft_raw.rename(columns={"Area": "Country"})

# From your inspection:
# Element = 'Use per area of cropland'
# Item    = 'Nutrient nitrogen N (total)'
# Unit    = 'kg/ha'
required_cols = {"Country", "Year", "Element", "Item", "Unit", "Value"}
missing = required_cols - set(ft_raw.columns)
if missing:
    raise ValueError(f"Fertilizer file missing columns: {missing}")

ft = ft_raw[
    (ft_raw["Element"] == "Use per area of cropland") &
    (ft_raw["Item"] == "Nutrient nitrogen N (total)") &
    (ft_raw["Unit"] == "kg/ha")
].copy()

ft = ft.rename(columns={"Value": "Fertilizer_N_kg_ha"})
ft["Year"] = ft["Year"].astype(int)

ft_clean = ft[["Country", "Year", "Fertilizer_N_kg_ha"]].dropna()
ft_clean = ft_clean[ft_clean["Country"].isin(countries_keep)]
ft_clean = ft_clean[(ft_clean["Year"] >= 2010) & (ft_clean["Year"] <= 2023)]

ft_clean.to_csv(fert_out, index=False)

print("Saved:", fert_out)
print(ft_clean.head())
print("Fert countries:", ft_clean["Country"].unique())

# ============================
# 5) SOIL INDEX (DEFAULTS)
# ============================
print("\n=== SOIL INDEX (DEFAULTS) ===")

soil_data = [
    {"Country": "Mozambique",   "SoilIndex": 0.72},
    {"Country": "South Africa", "SoilIndex": 0.68},
    {"Country": "Kenya",        "SoilIndex": 0.75},
    {"Country": "Brazil",       "SoilIndex": 0.77},
]
soil_df = pd.DataFrame(soil_data)
soil_df.to_csv(soil_out, index=False)

print("Saved:", soil_out)
print(soil_df)

print("\n✅ All H1 inputs cleaned. Next step: run your merge script.")
