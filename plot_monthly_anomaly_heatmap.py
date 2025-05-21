import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV ファイルを指定（例: 東京）
csv_path = "data/tokyo_monthly_avg_temp.csv"

# データ読み込み
df = pd.read_csv(csv_path)

# 欠損データ除外
df = df.dropna(subset=["avg_temp"])

# year × month の形式に変換
pivot_df = df.pivot(index="year", columns="month", values="avg_temp")

# 各月の平均値を基準に偏差（anomaly）を計算
monthly_mean = pivot_df.mean()
anomaly_df = pivot_df - monthly_mean

# プロット
plt.figure(figsize=(12, 8))
sns.heatmap(
    anomaly_df,
    cmap="coolwarm",  # 暖色=高温, 寒色=低温
    center=0,  # 偏差の中心を0に
    linewidths=0.3,
    cbar_kws={"label": "Anomaly (°C)"},
)
plt.title("Monthly Temperature Anomaly in Tokyo (vs Monthly Mean)")
plt.xlabel("Month")
plt.ylabel("Year")
plt.tight_layout()
plt.show()
