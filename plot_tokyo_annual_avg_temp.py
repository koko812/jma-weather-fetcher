import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("data/tokyo_monthly_avg_temp.csv")

# Calculate annual average temperature
df_avg_by_year = df.groupby("year")["avg_temp"].mean().reset_index()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_avg_by_year["year"], df_avg_by_year["avg_temp"], marker="o")
plt.title("Annual Average Temperature in Tokyo (1980–2023)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Average Temperature (°C)", fontsize=12)
plt.grid(True)
plt.tight_layout()

# Save the figure
output_path = "plots/tokyo_annual_avg_temperature_1980_2023.png"
plt.savefig(output_path)
plt.show()

print(f"✅ Figure saved to: {output_path}")
