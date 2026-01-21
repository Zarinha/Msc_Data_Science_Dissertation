import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ------------------------------------------------
# 0. Paths
# ------------------------------------------------
base_dir = Path(r"C:\Users\jessi\Dissertation")
data_dir = base_dir / "data" / "processed"
fig_dir  = base_dir / "figures"

fig_dir.mkdir(parents=True, exist_ok=True)

results_file = data_dir / "H2_monte_carlo_results.csv"

# ------------------------------------------------
# 1. Load results
# ------------------------------------------------
df = pd.read_csv(results_file)

# Rename columns for nicer labels
df.columns = [c.replace("profit_", "") for c in df.columns]

countries = df.columns.tolist()

# Style
sns.set(style="whitegrid")
plt.rcParams["figure.dpi"] = 150

# ------------------------------------------------
# 2. Plot distribution for each country
# ------------------------------------------------
for country in countries:
    plt.figure(figsize=(8,5))
    sns.histplot(df[country], bins=40, kde=True, color="steelblue")
    plt.title(f"Profit Distribution – {country.replace('_',' ')}", fontsize=14)
    plt.xlabel("Profit (USD)", fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.tight_layout()
    
    out_path = fig_dir / f"H2_profit_distribution_{country}.png"
    plt.savefig(out_path, dpi=300)
    plt.close()

# ------------------------------------------------
# 3. Combined violin plot (comparison)
# ------------------------------------------------
plt.figure(figsize=(10,6))
sns.violinplot(data=df, palette="Set2", cut=0)
plt.title("Profit Distribution Comparison – H2 Monte Carlo", fontsize=14)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Profit (USD)", fontsize=12)
plt.tight_layout()

out_path = fig_dir / "H2_profit_violin_comparison.png"
plt.savefig(out_path, dpi=300)
plt.close()

# ------------------------------------------------
# 4. Combined boxplot (clean and simple)
# ------------------------------------------------
plt.figure(figsize=(10,6))
sns.boxplot(data=df, palette="Set3")
plt.title("Monte Carlo Profit Outcomes – Boxplot", fontsize=14)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Profit (USD)", fontsize=12)
plt.tight_layout()

out_path = fig_dir / "H2_profit_boxplot_comparison.png"
plt.savefig(out_path, dpi=300)
plt.close()

print("Plots saved to:", fig_dir)
