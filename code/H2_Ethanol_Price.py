import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

# 1. Load CSV
file_path = r"C:\Users\jessi\Dissertation\data\raw\ethanol_prices\cepea-consulta-20251116170155.csv"
df = pd.read_csv(file_path)

prices = df["price_usd_litre"].astype(float).values

# 2. Min, max, mode (via KDE)
p_min = prices.min()
p_max = prices.max()

kde = gaussian_kde(prices)
x_grid = np.linspace(p_min, p_max, 500)
p_mode = x_grid[np.argmax(kde(x_grid))]

print("Min  :", round(p_min, 4))
print("Mode :", round(p_mode, 4))
print("Max  :", round(p_max, 4))
print(f"\nTriangular({p_min:.4f}, {p_mode:.4f}, {p_max:.4f})")

# 3. Save cleaned dataset
out_path = r"C:\Users\jessi\Dissertation\data\processed\ethanol_prices_clean.csv"
df.to_csv(out_path, index=False)
print(f"\nSaved cleaned file to: {out_path}")

# 4. Optional plot
plt.figure()
plt.hist(prices, bins=10, density=True, alpha=0.5)
plt.plot(x_grid, kde(x_grid))
plt.xlabel("USD per litre")
plt.ylabel("Density")
plt.title("Hydrous ethanol price distribution (CEPEA, 2010–2024)")
plt.grid(True)
plt.show()
