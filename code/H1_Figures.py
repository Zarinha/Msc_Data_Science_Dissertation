import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# ============================
# Paths
# ============================
data_path = r"C:\Users\jessi\Dissertation\data\climate_yield\cleaned\panel_H1_2010_2023.csv"
fig_dir = r"C:\Users\jessi\Dissertation\figures"

os.makedirs(fig_dir, exist_ok=True)

# ============================
# Load data
# ============================
df = pd.read_csv(data_path)

countries = df["Country"].unique()
colors = {
    "Brazil": "tab:green",
    "Kenya": "tab:blue",
    "Mozambique": "tab:orange",
    "South Africa": "tab:red"
}

# ============================
# Function to plot scatter + OLS line
# ============================
def plot_relationship(xvar, yvar, xlabel, ylabel, filename):
    plt.figure(figsize=(8, 6))

    # Plot points per country
    for c in countries:
        subset = df[df["Country"] == c]
        plt.scatter(subset[xvar], subset[yvar],
                    label=c, s=40, alpha=0.7, color=colors[c])

        # Regression line per country
        x = subset[xvar].values
        y = subset[yvar].values

        if len(x) > 1:
            slope, intercept = np.polyfit(x, y, 1)
            xs = np.linspace(min(x), max(x), 100)
            ys = slope * xs + intercept
            plt.plot(xs, ys, color=colors[c], linewidth=1.5)

    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    save_path = os.path.join(fig_dir, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved: {save_path}")

# ============================
# Generate Figures
# ============================

# FIGURE 4.1
plot_relationship(
    xvar="Rain_mm",
    yvar="Yield_t_ha",
    xlabel="Annual Precipitation (mm)",
    ylabel="Sugarcane Yield (t/ha)",
    filename="Figure_4_1_Yield_vs_Rain.png"
)

# FIGURE 4.2
plot_relationship(
    xvar="Temp_C",
    yvar="Yield_t_ha",
    xlabel="Mean Annual Temperature (°C)",
    ylabel="Sugarcane Yield (t/ha)",
    filename="Figure_4_2_Yield_vs_Temperature.png"
)

# FIGURE 4.3
plot_relationship(
    xvar="Fertilizer_N_kg_ha",
    yvar="Yield_t_ha",
    xlabel="Nitrogen Application (kg N/ha)",
    ylabel="Sugarcane Yield (t/ha)",
    filename="Figure_4_3_Yield_vs_Fertilizer.png"
)

print("All figures generated successfully.")
