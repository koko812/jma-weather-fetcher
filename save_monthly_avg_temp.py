# save_monthly_avg_temps.py
import os
from scrape_tokyo_monthly_temp import fetch_monthly_temperature, save_to_csv

cities = {
    "tokyo": ("44", "47662"),
    "sapporo": ("14", "47412"),
    "naha": ("91", "47936"),
}

years = range(1920, 2024)

for name, (prec_no, block_no) in cities.items():
    print(f"📡 Fetching: {name}")
    all_data = []
    for y in years:
        result = fetch_monthly_temperature(prec_no, block_no, y)
        if result:
            all_data.extend(result)
    save_to_csv(all_data, f"data/{name}_monthly_avg_temp.csv")
    print(f"✅ Saved: data/{name}_monthly_avg_temp.csv")
