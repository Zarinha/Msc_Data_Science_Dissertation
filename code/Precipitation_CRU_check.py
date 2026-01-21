# Precipitation_CRU_check_fixed.py
# --------------------------------
# Reads CRU TS precipitation (.nc), builds area-weighted national annual totals (mm/yr)
# for Brazil, Kenya, Mozambique, South Africa; compares to World Bank climatology.

import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
import regionmask
from pathlib import Path

# ======== CONFIG (edit paths as needed) ========
CRU_FILES = [
    r"C:\Users\jessi\Dissertation\data\raw\cru_ts4.09.2001.2010.pre.dat.nc",
    r"C:\Users\jessi\Dissertation\data\raw\cru_ts4.09.2011.2020.pre.dat.nc",
    r"C:\Users\jessi\Dissertation\data\raw\cru_ts4.09.2021.2024.pre.dat.nc",
]

# Natural Earth Admin 0 – Countries (110m): download and point to the .shp path
NE_COUNTRIES_SHP = r"C:\Users\jessi\Dissertation\data\shapes\ne_110m_admin_0_countries.shp"

COUNTRIES = ["Brazil", "Kenya", "Mozambique", "South Africa"]

OUT_CSV = Path(r"C:\Users\jessi\Dissertation\data\processed\precip_cru_annual_QA_countries.csv")

WB_REF_MM = {  # World Bank avg precipitation in depth (mm/year) – climatology (constant)
    "Brazil": 1761,
    "Kenya": 630,
    "Mozambique": 1032,
    "South Africa": 495,
}

# ======== HELPERS ========
def to_lon180(da: xr.DataArray) -> xr.DataArray:
    """Convert 0..360 longitudes to -180..180 if needed, and sort by lon."""
    lon = da.lon
    if np.nanmin(lon) >= 0 and np.nanmax(lon) > 180:
        new_lon = (((lon + 180) % 360) - 180)
        # sort by numeric value
        order = np.argsort(new_lon)
        da = da.assign_coords(lon=new_lon.values).isel(lon=order)
    return da

def area_weights(lat: xr.DataArray) -> xr.DataArray:
    """Cosine(latitude) weights for area-mean on a lat-lon grid (not normalized)."""
    w = np.cos(np.deg2rad(lat))
    return xr.DataArray(w, coords={"lat": lat}, dims=("lat",))

# ======== MAIN ========
def main():
    # 1) Open CRU files & concat
    ds = xr.open_mfdataset(CRU_FILES, combine="by_coords", parallel=False)
    if "pre" not in ds:
        raise ValueError(f"'pre' not found in dataset variables: {list(ds.data_vars)}")
    pre = ds["pre"]  # units: mm/month; dims: time x lat x lon

    # Fix longitudes to -180..180 if needed
    pre = to_lon180(pre)

    print("CRU variable:", pre.name)
    print("Dims:", dict(pre.sizes))
    print("Time:", pd.to_datetime(pre.time.values[0]).date(), "→", pd.to_datetime(pre.time.values[-1]).date())
    print("Lat range:", float(pre.lat.min()), "to", float(pre.lat.max()))
    print("Lon range:", float(pre.lon.min()), "to", float(pre.lon.max()))

    # 2) Annual totals: mm/year = sum of monthly mm
    # Use 'YE' (year-end) to avoid deprecation warning
    pre_annual = pre.resample(time="YE").sum("time")  # dims: time x lat x lon

    # 3) Load Natural Earth shapefile (local)
    shp = Path(NE_COUNTRIES_SHP)
    if not shp.exists():
        raise FileNotFoundError(
            f"Natural Earth shapefile not found:\n{shp}\n"
            "Download Admin 0 – Countries (110m) and set NE_COUNTRIES_SHP to the .shp path."
        )
    world = gpd.read_file(shp).to_crs("EPSG:4326")

    # Natural Earth name column can be 'NAME' or 'ADMIN' depending on version
    name_col = "NAME" if "NAME" in world.columns else ("ADMIN" if "ADMIN" in world.columns else None)
    if name_col is None:
        raise ValueError(f"No suitable country name column found. Columns: {world.columns.tolist()}")

    gdf = world[world[name_col].isin(COUNTRIES)][[name_col, "geometry"]].reset_index(drop=True)
    gdf = gdf.rename(columns={name_col: "name"})

    found = gdf["name"].tolist()
    print("Matched countries in shapefile:", found)
    missing = set(COUNTRIES) - set(found)
    if missing:
        print("WARNING: Missing in shapefile:", missing)

    # 4) Build region mask (compatible with older regionmask API)
    regions = regionmask.from_geopandas(gdf, names="name")
    # mask: DataArray (lat x lon) with region indices (0..n-1), NaN outside
    mask = regions.mask(pre_annual.lon, pre_annual.lat)

    # Map from name to region index
    name_to_idx = {name: i for i, name in enumerate(regions.names)}

    # 5) Area weights (cos(lat)) → broadcast to 2D
    Wlat = area_weights(pre_annual.lat)
    W = Wlat.broadcast_like(pre_annual.isel(time=0))

    # 6) Area-weighted national precipitation (mm/year)
    rows = []
    for cname in gdf["name"]:
        ridx = name_to_idx[cname]
        rmask = (mask == ridx)

        # Apply mask
        pre_reg = pre_annual.where(rmask)
        W_reg = W.where(rmask)

        # Normalize weights per time slice
        wsum = W_reg.sum(dim=("lat", "lon"), skipna=True)
        Wn = W_reg / wsum

        # Area-weighted mean over lat/lon
        pre_nat = (pre_reg * Wn).sum(dim=("lat", "lon"), skipna=True)  # mm/year
        years = pd.to_datetime(pre_nat.time.values).year
        vals = pre_nat.values

        for y, v in zip(years, vals):
            if np.isfinite(v):
                rows.append({"Year": int(y), "Country": cname, "Rain_mm": float(v)})

    df = pd.DataFrame(rows).sort_values(["Country", "Year"]).reset_index(drop=True)

    # 7) QA summaries
    print("\n=== CRU annual precipitation summary (mm/yr) ===")
    print(df.groupby("Country")["Rain_mm"].agg(["min", "max", "mean"]).round(1))

    comp = (
        df.groupby("Country")["Rain_mm"].mean().round(1)
        .rename("CRU_mean_mm").to_frame()
        .assign(WB_mm=lambda t: t.index.map(WB_REF_MM.get))
        .assign(Diff_mm=lambda t: t["CRU_mean_mm"] - t["WB_mm"])
    )
    print("\nCRU mean (2001–2024) vs World Bank climatology (mm/yr):\n", comp)

    # Flag suspicious values
    sus = df[df["Rain_mm"] > 5000]
    if not sus.empty:
        print("\nWARNING: Suspicious annual totals (>5000 mm):")
        print(sus.head(10))

    # 8) Save
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print("\nSaved:", OUT_CSV)


if __name__ == "__main__":
    main()
