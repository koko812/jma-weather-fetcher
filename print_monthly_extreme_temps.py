import pandas as pd

# 東京の月別気温データを読み込み
df = pd.read_csv("data/tokyo_monthly_avg_temp.csv")
df = df.dropna(subset=["avg_temp"])

# 月ごとの処理
for month in range(1, 13):
    monthly = df[df["month"] == month]

    # 平均を計算
    monthly_mean = monthly["avg_temp"].mean()

    # 上位5件（暑い年）と下位5件（寒い年）
    hottest = monthly.nlargest(5, "avg_temp")
    coldest = monthly.nsmallest(5, "avg_temp")

    print(f"\n=== 📅 Month: {month} ===")
    print(f"📊 Monthly Mean (Entire Period): {monthly_mean:.2f} °C\n")

    print("🔥 Hottest Years:")
    for _, row in hottest.iterrows():
        diff = row["avg_temp"] - monthly_mean
        print(f" {int(row['year'])}: {row['avg_temp']:.2f} °C  (Δ {diff:+.2f})")

    print("\n❄️ Coldest Years:")
    for _, row in coldest.iterrows():
        diff = row["avg_temp"] - monthly_mean
        print(f" {int(row['year'])}: {row['avg_temp']:.2f} °C  (Δ {diff:+.2f})")
