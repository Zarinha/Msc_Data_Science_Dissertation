# save_cru_rain_to_cleaned.py
import pandas as pd
from pathlib import Path

qa_csv = Path(r"C:\Users\jessi\Dissertation\data\processed\precip_cru_annual_QA_countries.csv")
out_csv = Path(r"C:\Users\jessi\Dissertation\data\climate_yield\cleaned\rain_cru_annual_long.csv")

df = pd.read_csv(qa_csv)  # columns: Year, Country, Rain_mm
# keep only target countries & years
countries = ["Brazil","Kenya","Mozambique","South Africa"]
df = df[df["Country"].isin(countries)]
df = df[(df["Year"]>=2010) & (df["Year"]<=2023)]
out_csv.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_csv, index=False)
print("✅ Saved:", out_csv, df.shape)
