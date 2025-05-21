import pandas as pd
import matplotlib.pyplot as plt

# データ読み込み
df = pd.read_csv("data/tokyo_monthly_avg_temp.csv")

# 年と月のカラムを整数に
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)

# 年間平均
annual_avg = df.groupby("year")["avg_temp"].mean()

# 夏（7月・8月）と冬（1月・2月）の平均
summer = df[df["month"].isin([7, 8])].groupby("year")["avg_temp"].mean()
winter = df[df["month"].isin([1, 2])].groupby("year")["avg_temp"].mean()

# 可視化
plt.figure(figsize=(10, 6))
plt.plot(annual_avg.index, annual_avg.values, label="Annual Avg", marker="o")
plt.plot(summer.index, summer.values, label="Summer (Jul-Aug)", marker="o")
plt.plot(winter.index, winter.values, label="Winter (Jan-Feb)", marker="o")

plt.title("Tokyo Temperature Trends (1980–2023)")
plt.xlabel("Year")
plt.ylabel("Average Temperature (°C)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
