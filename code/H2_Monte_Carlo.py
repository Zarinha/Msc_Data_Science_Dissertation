import numpy as np
import pandas as pd
from pathlib import Path

# ------------------------------------------------
# 0. Paths (assumes this script is in /code)
# ------------------------------------------------
base_dir = Path(__file__).resolve().parents[1]  # ...\Dissertation
data_dir = base_dir / "data" / "processed"

ethanol_price_file = data_dir / "ethanol_prices_clean.csv"       # not strictly needed, kept for record
cp_file            = data_dir / "production_costs_clean.csv"
ct_file            = data_dir / "logistics_costs_clean.csv"
q_file             = data_dir / "export_volumes_clean.csv"

# ------------------------------------------------
# 1. Load Cp parameters from CSV
# ------------------------------------------------
cp_df = pd.read_csv(cp_file)

cp_mean = cp_df.loc[cp_df["parameter"] == "mean", "value"].iloc[0]
cp_std  = cp_df.loc[cp_df["parameter"] == "std_dev", "value"].iloc[0]

# ------------------------------------------------
# 2. Load Ct triangular parameters from CSV
# ------------------------------------------------
ct_df = pd.read_csv(ct_file)

ct_min  = ct_df.loc[ct_df["parameter"] == "min",  "value"].iloc[0]
ct_mode = ct_df.loc[ct_df["parameter"] == "mode", "value"].iloc[0]
ct_max  = ct_df.loc[ct_df["parameter"] == "max",  "value"].iloc[0]

# ------------------------------------------------
# 3. Load export volumes Q from CSV
# ------------------------------------------------
q_df = pd.read_csv(q_file)

# Make dict: {country: Q}
q_dict = dict(zip(q_df["country"], q_df["export_volume_litres"]))

# ------------------------------------------------
# 4. Ethanol price distribution (Pe) from CEPEA result
#    Pe ~ Triangular(0.3573, 0.4972, 0.7229)
# ------------------------------------------------
pe_min  = 0.3573
pe_mode = 0.4972
pe_max  = 0.7229

# ------------------------------------------------
# 5. Monte Carlo simulation
# ------------------------------------------------
N_ITER = 10_000
rng = np.random.default_rng(seed=42)

# Draws that are common to all countries (only Q differs)
pe_samples = rng.triangular(left=pe_min, mode=pe_mode, right=pe_max, size=N_ITER)
cp_samples = rng.normal(loc=cp_mean, scale=cp_std, size=N_ITER)
ct_samples = rng.triangular(left=ct_min, mode=ct_mode, right=ct_max, size=N_ITER)

margin_per_litre = pe_samples - cp_samples - ct_samples  # USD/L

results_list = []

for country, Q in q_dict.items():
    profit = margin_per_litre * Q  # total profit in USD

    # Summary stats
    mean_profit   = profit.mean()
    median_profit = np.median(profit)
    std_profit    = profit.std()
    p5            = np.percentile(profit, 5)
    p95           = np.percentile(profit, 95)
    prob_pos      = (profit > 0).mean()

    results_list.append({
        "country": country,
        "Q_litres": Q,
        "mean_profit_USD": mean_profit,
        "median_profit_USD": median_profit,
        "std_profit_USD": std_profit,
        "p5_profit_USD": p5,
        "p95_profit_USD": p95,
        "prob_profit_positive": prob_pos
    })

# ------------------------------------------------
# 6. Save outputs
# ------------------------------------------------
summary_df = pd.DataFrame(results_list)
summary_path = data_dir / "H2_monte_carlo_summary.csv"
summary_df.to_csv(summary_path, index=False)

# Optional: save full profit distributions per country
full_results = {}
for country, Q in q_dict.items():
    full_results[f"profit_{country}"] = margin_per_litre * Q

full_df = pd.DataFrame(full_results)
full_path = data_dir / "H2_monte_carlo_results.csv"
full_df.to_csv(full_path, index=False)

print("Monte Carlo finished.")
print("Summary saved to:", summary_path)
print("Full results saved to:", full_path)
print("\nSummary:")
print(summary_df)
