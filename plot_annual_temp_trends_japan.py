import pandas as pd
import matplotlib.pyplot as plt

# ファイルパス（適宜変更）
tokyo_csv = "data/tokyo_monthly_avg_temp.csv"
sapporo_csv = "data/sapporo_monthly_avg_temp.csv"
naha_csv = "data/naha_monthly_avg_temp.csv"

# CSV 読み込み
def load_and_aggregate(path, city_name):
    df = pd.read_csv(path)
    df = df.dropna(subset=["avg_temp"])
    df["city"] = city_name
    grouped = df.groupby("year")["avg_temp"]

    # 12ヶ月分そろっている年のみ平均を取る
    valid_years = grouped.count() == 12
    return (
        grouped.mean()[valid_years]
        .reset_index()
        .rename(columns={"avg_temp": "annual_avg_temp"})
    )


tokyo = load_and_aggregate(tokyo_csv, "Tokyo")
sapporo = load_and_aggregate(sapporo_csv, "Sapporo")
naha = load_and_aggregate(naha_csv, "Naha")

# 結合
all_df = pd.concat([tokyo.assign(city="Tokyo"),
                    sapporo.assign(city="Sapporo"),
                    naha.assign(city="Naha")])

# プロット
plt.figure(figsize=(10, 6))
for city, group in all_df.groupby("city"):
    plt.plot(group["year"], group["annual_avg_temp"], marker="o", label=city)

plt.title("Annual Average Temperature Trends (Tokyo, Sapporo, Naha)")
plt.xlabel("Year")
plt.ylabel("Average Temperature (°C)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
