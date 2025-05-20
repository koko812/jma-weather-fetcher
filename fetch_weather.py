
import argparse
import os

def fetch_and_save_weather(station, date, output_path):
    # TODO: 気象庁のCSV取得URLを構築し、ダウンロード＆保存
    print(f"Fetching weather data for station {station} on {date} ...")
    print(f"Saving to {output_path} ...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--station", required=True, help="気象庁の地点番号")
    parser.add_argument("--date", required=True, help="取得する日付（YYYY-MM-DD）")
    parser.add_argument("--output", required=True, help="CSV出力先ファイルパス")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    fetch_and_save_weather(args.station, args.date, args.output)

