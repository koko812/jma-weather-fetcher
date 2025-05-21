import argparse
import os
import sys
from v2_weather_fetcher import fetch_jma_csv
from parse_jma_table import parse_weather_html_to_csv


def run(prec_no, block_no, date_str, output_path):
    tmp_path = "tmp.html"

    # ステップ1: HTML取得
    print("\n📥 ステップ1: HTML取得中...")
    fetch_jma_csv(prec_no, block_no, date_str, output_html_path=tmp_path)  # ✅ 修正済み
    if not os.path.exists(tmp_path):
        print("❌ HTMLファイルが見つかりません")
        sys.exit(1)

    # ステップ2: HTML -> CSV変換
    print("\n🧪 ステップ2: HTML -> CSV変換中...")
    success = parse_weather_html_to_csv(tmp_path, output_path)
    if success:
        print(f"✅ 変換成功: {output_path}")
    else:
        print("❌ 変換に失敗しました")
        sys.exit(1)

    # ステップ3: 一時ファイル削除（必要なら）
    os.remove(tmp_path)
    print("\n🧹 一時ファイルを削除しました")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prec", required=True, help="都道府県番号（例：44=東京）")
    parser.add_argument("--block", required=True, help="地点番号（例：47662）")
    parser.add_argument("--date", required=True, help="日付 (YYYY-MM-DD)")
    parser.add_argument("--output", required=True, help="CSVの出力先パス")
    args = parser.parse_args()

    run(args.prec, args.block, args.date, args.output)
