import pandas as pd

# Load filtered dataset
df = pd.read_csv(r"C:\Users\jessi\Dissertation\data\processed\H4_EU_grid_CI_filtered.csv")

# Compute mean for 2022–2024
df['CI_gCO2_per_kWh_2022_2024_avg'] = df[['2022', '2023', '2024']].mean(axis=1)

# Keep only necessary columns
df_processed = df[['Countries', 'CI_gCO2_per_kWh_2022_2024_avg']]

# Save processed file
output_path = r"C:\Users\jessi\Dissertation\data\processed\H4_EU_grid_CI_processed.csv"
df_processed.to_csv(output_path, index=False)

print("Processed file saved to:", output_path)
