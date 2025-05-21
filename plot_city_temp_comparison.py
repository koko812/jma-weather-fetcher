import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
tokyo = pd.read_csv("data/tokyo_monthly_avg_temp.csv")
sapporo = pd.read_csv("data/sapporo_monthly_avg_temp.csv")
naha = pd.read_csv("data/naha_monthly_avg_temp.csv")

# Add city labels
tokyo["city"] = "Tokyo"
sapporo["city"] = "Sapporo"
naha["city"] = "Naha"

# Combine all
df = pd.concat([tokyo, sapporo, naha])

# Filter only latest 3 years for clarity (optional)
latest_years = df["year"].max() - 2
df_recent = df[df["year"] >= latest_years]

# Plot: Monthly average temperature per city
plt.figure(figsize=(12, 6))
for city in ["Tokyo", "Sapporo", "Naha"]:
    monthly_avg = (
        df_recent[df_recent["city"] == city]
        .groupby("month")["avg_temp"]
        .mean()
    )
    plt.plot(monthly_avg.index, monthly_avg.values, marker="o", label=city)

plt.title("Average Monthly Temperature Comparison (Recent 3 Years)")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.xticks(range(1, 13))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("output/monthly_temp_comparison.png")
plt.show()
