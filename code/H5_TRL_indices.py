import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Create the TRL dataset
# -----------------------------
data = {
    "Indicator": [
        "Flex-fuel vehicle (FFV) penetration",
        "Fueling infrastructure (E85 stations per 1 000 vehicles)",
        "RED II policy alignment (biofuel mandates & targets)",
        "Sustainability certification systems in place",
        "Distribution readiness (storage & blending capacity)",
        "R&D and innovation programs on bioethanol",
    ],
    "Sweden":  [9, 9, 9, 8, 9, 8],
    "Germany": [5, 6, 8, 7, 6, 7],
    "France":  [4, 5, 8, 6, 6, 6],
    "Italy":   [3, 4, 7, 6, 5, 6],
}

df_trl = pd.DataFrame(data)

# -----------------------------
# 2. Compute composite TRL index (Eq. 3.6 with equal weights)
# -----------------------------
trl_index = df_trl[["Sweden", "Germany", "France", "Italy"]].mean()
trl_index_rounded = trl_index.round(1)

df_trl_index = pd.DataFrame({
    "Country": trl_index_rounded.index,
    "TRL_Index": trl_index_rounded.values
})

print("TRL index table:")
print(df_trl_index)

# -----------------------------
# 3. Save TRL index results to CSV
# -----------------------------
output_csv = "TRL_index_summary.csv"
df_trl_index.to_csv(output_csv, index=False)
print(f"\nTRL index results saved to: {output_csv}")

# -----------------------------
# 4. Create and save bar chart of TRL indices
# -----------------------------
plt.figure(figsize=(6, 4))
plt.bar(df_trl_index["Country"], df_trl_index["TRL_Index"])
plt.xlabel("Country")
plt.ylabel("Composite TRL Index (0–9)")
plt.title("Technology Readiness Level (TRL) for Ethanol Adoption in Europe")
plt.ylim(0, 9)

# Annotate each bar with its value
for i, row in df_trl_index.iterrows():
    plt.text(
        i,
        row["TRL_Index"] + 0.1,
        f"{row['TRL_Index']}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()
output_png = "TRL_index_bar_chart.png"
plt.savefig(output_png, dpi=300)
plt.close()

print(f"Bar chart saved to: {output_png}")
