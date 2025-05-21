import argparse
import os
import requests

def fetch_jma_csv(station: str, date: str, output_path: str):
    yyyymmdd = date.replace("-", "")
    yyyy = date[:4]
    url = f"https://www.data.jma.go.jp/stats/data/csv/{yyyy}/{station}/{station}_{yyyymmdd}.csv"

    print(f"📡 ダウンロード中: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ 保存しました: {output_path}")
    else:
        print(f"❌ 取得失敗（ステータス: {response.status_code}）: URL = {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--station", required=True, help="気象庁の地点番号")
    parser.add_argument("--date", required=True, help="日付 (例: 2024-05-20)")
    parser.add_argument("--output", required=True, help="CSVの出力先パス")
    args = parser.parse_args()

    fetch_jma_csv(args.station, args.date, args.output)
