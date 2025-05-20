# 🌤 JMA Weather Fetcher

気象局の「過去の気象データ検索」から、特定地点の過去の天気データを取得してCSVに保存するPythonツールです。

---

## 📦 セットアップ

```bash
git clone https://github.com/yourname/jma_weather_fetcher.git
cd jma_weather_fetcher
python -m venv venv
source venv/bin/activate  # Windowsの方は venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 使用方法（予定）

```bash
python fetch_weather.py --station 47662 --date 2024-05-20 --output data/tokyo_20240520.csv
```

---

## 🔧 引数（予定）

| 引数          | 内容                         |
| ----------- | -------------------------- |
| `--station` | 地点番号（例：47662 は東京）          |
| `--date`    | 対象日付（例：2024-05-20）         |
| `--output`  | 保存ファイルパス（例：data/tokyo.csv） |

---

## 📊 今後の展望

* SQLite への保存機能
* `matplotlib` によるグラフ表示
* 降水量・湿度など他の気象項目への対応
* 自動スケジューリング対応（cronなど）

