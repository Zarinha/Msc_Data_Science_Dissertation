import pandas as pd, numpy as np
import statsmodels.formula.api as smf
from pathlib import Path

df = pd.read_csv(r"C:\Users\jessi\Dissertation\data\climate_yield\cleaned\panel_H1_2010_2023.csv")

# numeric + drop NA
for c in ["Rain_mm","Temp_C","Fertilizer_N_kg_ha","SoilIndex","Yield_t_ha","Year"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["Yield_t_ha","Rain_mm","Temp_C","Fertilizer_N_kg_ha","SoilIndex","Country"])

# z-scores
for c in ["Rain_mm","Temp_C","Fertilizer_N_kg_ha","SoilIndex"]:
    mu, sd = df[c].mean(), df[c].std()
    df[c+"_z"] = (df[c]-mu)/sd if sd>0 else df[c]

# 1) Pooled OLS (includes SoilIndex)
m_pooled = smf.ols("Yield_t_ha ~ Rain_mm_z + Temp_C_z + Fertilizer_N_kg_ha_z + SoilIndex_z", data=df).fit(cov_type="HC1")
print("\n=== H1 Pooled OLS (HC1) ===")
print(m_pooled.summary())

# 2) Country FE OLS (drop SoilIndex to avoid collinearity)
m_fe = smf.ols("Yield_t_ha ~ Rain_mm_z + Temp_C_z + Fertilizer_N_kg_ha_z + C(Country)", data=df).fit(cov_type="HC1")
print("\n=== H1 OLS with Country FE (HC1, SoilIndex omitted) ===")
print(m_fe.summary())
