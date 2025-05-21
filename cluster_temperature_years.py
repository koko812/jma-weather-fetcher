import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

# CSV から読み込み（東京の12ヶ月ベクトル形式）
df = pd.read_csv("data/tokyo_monthly_avg_temp.csv")

# 欠損がない年だけを抽出（12ヶ月分そろっている年）
df_clean = df.dropna(subset=["avg_temp"])
pivot_df = df_clean.pivot(index="year", columns="month", values="avg_temp").dropna()

# クラスタ数を仮に 4 と設定（変更可）
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(pivot_df)

# t-SNE で 2次元に次元圧縮
tsne = TSNE(n_components=2, perplexity=10, random_state=42)
embedding = tsne.fit_transform(pivot_df)

# データフレームにまとめ
plot_df = pd.DataFrame(embedding, columns=["x", "y"])
plot_df["year"] = pivot_df.index
plot_df["cluster"] = clusters

# プロット
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=plot_df,
    x="x", y="y",
    hue="cluster",
    palette="Set2",
    s=100,
    alpha=0.8,
    legend="full"
)

# 年のラベルもつける（任意）
for _, row in plot_df.iterrows():
    plt.text(row["x"], row["y"], str(int(row["year"])), fontsize=7, alpha=0.6)

plt.title("t-SNE Clustering of Yearly Temperature Profiles (Tokyo)")
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.tight_layout()
plt.show()
