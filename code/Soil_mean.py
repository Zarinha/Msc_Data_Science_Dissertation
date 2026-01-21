import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import pandas as pd
from pathlib import Path

# 1. Paths
raster_path = Path(r"C:\Users\jessi\Dissertation\data\raw\HWSD2.bil")
shp_path    = Path(r"C:\Users\jessi\Dissertation\data\shapes\ne_10m_admin_0_countries.shp")
out_path    = Path(r"C:\Users\jessi\Dissertation\data\climate_yield\cleaned\soil_index_countries.csv")

# 2. Load raster (force ESRI BIL driver)
with rasterio.open(raster_path, driver="EHdr") as src:
    soil_raster = src.read(1)
    raster_crs = src.crs
    raster_transform = src.transform
    nodata = src.nodata


# 3. Load countries shapefile and select 4 countries
world = gpd.read_file(shp_path)
countries = ["Mozambique", "South Africa", "Kenya", "Brazil"]
gdf = world[world["NAME"].isin(countries)].copy()

# 4. Reproject polygons to raster CRS
gdf = gdf.to_crs(raster_crs)

results = []

# 5. Loop over countries and compute mean soil value inside polygon
with rasterio.open(raster_path) as src:
    for _, row in gdf.iterrows():
        country_name = row["NAME"]
        geom = [row["geometry"]]

        # Mask raster with polygon
        out_image, out_transform = mask(src, geom, crop=True)
        data = out_image[0]

        # Replace nodata with NaN
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)

        # Compute mean of valid pixels
        mean_val = float(np.nanmean(data))

        results.append({"Country": country_name, "SoilRawMean": mean_val})

# 6. Build DataFrame and (optionally) normalize to 0–1 index
df = pd.DataFrame(results)

# Normalize soil values to 0–1 index for use as S_t (optional but convenient)
min_val = df["SoilRawMean"].min()
max_val = df["SoilRawMean"].max()
df["SoilIndex_0_1"] = (df["SoilRawMean"] - min_val) / (max_val - min_val)

# 7. Save to CSV
out_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_path, index=False)

print("✅ Saved:", out_path)
print(df)
