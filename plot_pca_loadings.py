import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# CSV 読み込み
df = pd.read_csv("data/tokyo_monthly_avg_temp.csv")

# 年ごと × 月 のピボット
pivot_df = (
    df.dropna(subset=["avg_temp"])
    .pivot(index="year", columns="month", values="avg_temp")
)

# 欠損のある年（行）を除外
pivot_df = pivot_df.dropna()

# PCA 実行
pca = PCA(n_components=2)
pca_result = pca.fit_transform(pivot_df)

# 寄与率（分散比）
explained_ratio = pca.explained_variance_ratio_

# 各主成分の各月への寄与（loading）
loadings = pd.DataFrame(
    pca.components_,
    columns=[f"{month}月" for month in pivot_df.columns],
    index=["PC1", "PC2"]
).T

# プロット①：寄与率の棒グラフ
plt.figure(figsize=(6, 4))
plt.bar(["PC1", "PC2"], explained_ratio * 100)
plt.ylabel("Explained Variance Ratio (%)")
plt.title("Explained Variance by Principal Components")
plt.grid(True)
plt.tight_layout()
plt.show()

# プロット②：各月の loading（寄与度）
plt.figure(figsize=(10, 5))
loadings.plot(kind="bar")
plt.ylabel("Contribution")
plt.title("Monthly Contributions to PC1 and PC2")
plt.grid(True)
plt.tight_layout()
plt.show()
