import numpy as np
import pandas as pd
from netCDF4 import Dataset
from pathlib import Path

# 1. File paths
data_dir = Path(r"C:\Users\jessi\Dissertation\data\raw")
files = [
    data_dir / "cru_ts4.09.2001.2010.tmp.dat.nc",
    data_dir / "cru_ts4.09.2011.2020.tmp.dat.nc",
    data_dir / "cru_ts4.09.2021.2024.tmp.dat.nc",
]

# 2. Capital coordinates (representative point per country)
coords = {
    "Mozambique": {"lat": -25.97, "lon": 32.58},   # Maputo
    "South Africa": {"lat": -25.74, "lon": 28.19}, # Pretoria
    "Kenya": {"lat": -1.29, "lon": 36.82},         # Nairobi
    "Brazil": {"lat": -15.78, "lon": -47.93},      # Brasília
}

all_series = {country: [] for country in coords.keys()}
all_years = []

# 3. Loop over files and extract 1D time series for each country
for f in files:
    print(f"Reading {f} ...")
    ds = Dataset(f, "r")

    tmp = ds.variables["tmp"]    # shape: time x lat x lon
    lat = ds.variables["lat"][:] # 1D
    lon = ds.variables["lon"][:] # 1D
    time = ds.variables["time"][:]  # monthly steps since ref (not used in detail)

    ntime = tmp.shape[0]

    # CRU time is monthly; create month index starting from some base year
    # Easier: infer years from a starting year in the filename
    # Example filenames: cru_ts4.09.2001.2010.tmp.dat.nc
    name = f.name
    start_year = int(name.split(".")[2].split(".")[0])  # "2001"
    end_year = int(name.split(".")[3].split(".")[0])    # "2010"
    years = np.arange(start_year, end_year + 1)

    # check monthly count
    assert ntime == len(years) * 12, "unexpected time dimension length"

    # create array of year per monthly index
    year_for_step = np.repeat(years, 12)

    for country, c in coords.items():
        # find nearest indices
        i_lat = np.abs(lat - c["lat"]).argmin()
        i_lon = np.abs(lon - c["lon"]).argmin()

        # extract monthly temp series for that grid cell (1D)
        ts_monthly = tmp[:, i_lat, i_lon]  # shape: (time,)

        # build DataFrame for this file and country
        df = pd.DataFrame({
            "Year": year_for_step,
            "Temp_C": ts_monthly
        })

        # annual mean
        df_annual = df.groupby("Year")["Temp_C"].mean()

        # store
        for y, v in df_annual.items():
            all_series.setdefault(country, [])
            all_series[country].append((y, float(v)))

    ds.close()

# 4. Combine all years and countries into a single DataFrame
rows = {}
for country, pairs in all_series.items():
    for year, value in pairs:
        rows.setdefault(year, {})[country] = value

years_sorted = sorted(rows.keys())
data = []
for y in years_sorted:
    row = {"Year": y}
    row.update(rows[y])
    data.append(row)

df_final = pd.DataFrame(data)
df_final = df_final.sort_values("Year")

# 5. Save to CSV
out_path = Path(r"C:\Users\jessi\Dissertation\data\climate_yield\cleaned\cru_annual_temp_countries.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)
df_final.to_csv(out_path, index=False)

print("✅ Saved:", out_path)
print(df_final.head())
