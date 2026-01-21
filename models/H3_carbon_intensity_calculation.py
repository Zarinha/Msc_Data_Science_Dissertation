import os
import pandas as pd

# ------------------------------------------------------------------
# 1. Paths and filenames
# ------------------------------------------------------------------
DATA_DIR = r"C:\Users\jessi\Dissertation\data\processed"

EMISSION_FACTORS_FILE = "H3_Emission_Factors.csv"
TRANSPORT_FILE = "H3_Transport_Africa_EU.csv"
DISTANCES_FILE = "H3_Shipping_Distances_km.csv"

OUTPUT_FILE = "H3_CI_GHG_Results.csv"

# ------------------------------------------------------------------
# 2. Load input data
# ------------------------------------------------------------------
emission_factors_path = os.path.join(DATA_DIR, EMISSION_FACTORS_FILE)
transport_path = os.path.join(DATA_DIR, TRANSPORT_FILE)
distances_path = os.path.join(DATA_DIR, DISTANCES_FILE)

em = pd.read_csv(emission_factors_path)
tr = pd.read_csv(transport_path)
dist = pd.read_csv(distances_path)

# ------------------------------------------------------------------
# 3. Extract scalar emission factors from H3_Emission_Factors.csv
# ------------------------------------------------------------------
def get_factor(symbol: str) -> float:
    """Helper to pull a single numeric factor by Symbol."""
    value = em.loc[em["Symbol"] == symbol, "Value_gCO2e_MJ"]
    if value.empty:
        raise ValueError(f"Symbol '{symbol}' not found in {EMISSION_FACTORS_FILE}")
    return float(value.iloc[0])

E_CULT = get_factor("E_cult")         # cultivation
E_PROC = get_factor("E_proc")         # processing
E_OFFSET = get_factor("E_offset")     # cogeneration offset (negative)
CI_GASOLINE = get_factor("CI_gasoline")

print("Loaded emission factors:")
print(f"  E_cult     = {E_CULT} gCO2e/MJ")
print(f"  E_proc     = {E_PROC} gCO2e/MJ")
print(f"  E_offset   = {E_OFFSET} gCO2e/MJ")
print(f"  CI_gasoline= {CI_GASOLINE} gCO2e/MJ\n")

# ------------------------------------------------------------------
# 4. Merge transport data with shipping distances
# ------------------------------------------------------------------
# Both TRANSPORT_FILE and DISTANCES_FILE must share 'Route_ID'
merged = tr.merge(dist, on="Route_ID", how="left", suffixes=("", "_dist"))

# Check for missing distances (optional sanity check)
if merged["Distance_km"].isna().any():
    missing_routes = merged.loc[merged["Distance_km"].isna(), "Route_ID"].unique()
    print("Warning: Missing distances for Route_ID(s):", missing_routes)

# ------------------------------------------------------------------
# 5. Compute CI_ethanol and GHG reduction for each route
# ------------------------------------------------------------------
# Eq. 3.3: CI_ethanol = E_cult + E_proc + E_transp - E_offset
merged["CI_ethanol_gCO2e_MJ"] = (
    E_CULT
    + E_PROC
    + merged["Value_gCO2e_MJ"]    # route-specific transport factor
    - E_OFFSET                    # note: offset is negative in the CSV
)

# Eq. 3.4: GHG_reduction = 1 - CI_ethanol / CI_gasoline
merged["GHG_reduction_fraction"] = 1 - merged["CI_ethanol_gCO2e_MJ"] / CI_GASOLINE
merged["GHG_reduction_percent"] = merged["GHG_reduction_fraction"] * 100

# RED II compliance (65% minimum reduction)
REDII_THRESHOLD = 65.0
merged["REDII_Compliant"] = merged["GHG_reduction_percent"] >= REDII_THRESHOLD

# ------------------------------------------------------------------
# 6. Select and reorder columns for output
# ------------------------------------------------------------------
output_cols = [
    "Route_ID",
    "Exporting_Country",
    "Origin_Port",
    "Destination_Port",
    "Distance_km",
    "Distance_nautical_miles",
    "Transport_Stage",
    "Value_gCO2e_MJ",          # transport emissions
    "CI_ethanol_gCO2e_MJ",
    "GHG_reduction_percent",
    "REDII_Compliant",
    "Description",
    "Source"
]

results = merged[output_cols].copy()

# Round key numeric columns for nicer tables
results["CI_ethanol_gCO2e_MJ"] = results["CI_ethanol_gCO2e_MJ"].round(2)
results["GHG_reduction_percent"] = results["GHG_reduction_percent"].round(1)
results["Distance_km"] = results["Distance_km"].round(0)
results["Distance_nautical_miles"] = results["Distance_nautical_miles"].round(0)
results["Value_gCO2e_MJ"] = results["Value_gCO2e_MJ"].round(2)

# ------------------------------------------------------------------
# 7. Save output to the same folder
# ------------------------------------------------------------------
output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
results.to_csv(output_path, index=False)

print(f"H3 results saved to:\n  {output_path}\n")
print("Preview:")
print(results)
