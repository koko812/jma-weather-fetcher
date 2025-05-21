import pandas as pd
import matplotlib.pyplot as plt

city_files = {
    "Tokyo": "data/tokyo_monthly_avg_temp.csv",
    "Sapporo": "data/sapporo_monthly_avg_temp.csv",
    "Naha": "data/naha_monthly_avg_temp.csv",
}

city_styles = {
    "Tokyo": {"color": "tab:blue"},
    "Sapporo": {"color": "tab:green"},
    "Naha": {"color": "tab:purple"},
}

plt.figure(figsize=(10, 6))

for city, filepath in city_files.items():
    df = pd.read_csv(filepath)

    # 欠損を含む月を除外
    df_valid = df.dropna(subset=["avg_temp"])

    # 年ごとの月数と気温平均を集計し、12ヶ月揃っている年のみ残す
    yearly = (
        df_valid.groupby("year")
        .agg(month_count=("month", "count"), avg_temp=("avg_temp", "mean"))
        .reset_index()
    )
    annual_df = yearly[yearly["month_count"] == 12]

    # 実測値
    plt.plot(
        annual_df["year"],
        annual_df["avg_temp"],
        marker="o",
        linestyle="-",
        linewidth=1.2,
        color=city_styles[city]["color"],
        alpha=0.5,
        label=f"{city} Avg",
    )

    # 移動平均（5年）
    ma = annual_df["avg_temp"].rolling(window=5, min_periods=5).mean()
    plt.plot(
        annual_df["year"],
        ma,
        linestyle="-",
        linewidth=2.2,
        color=city_styles[city]["color"],
        label=f"{city} 5yr MA",
    )

plt.title("Annual Average Temperature with 5-Year Moving Average")
plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
