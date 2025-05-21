from bs4 import BeautifulSoup
import csv


def parse_weather_html_to_csv(html_path, output_csv_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        table = soup.select_one("#tablefix1")
        if not table:
            print("❌ 気象データの表が見つかりません")
            return False

        # ヘッダー取得
        headers = []
        for th in table.select("tr.mtx")[0].find_all("th"):
            text = th.get_text(strip=True).replace("\n", " ")
            headers.append(text)

        # データ行の抽出
        rows = []
        for tr in table.select("tr.mtx")[2:]:
            row = [td.get_text(strip=True).replace("\n", " ") for td in tr.find_all("td")]
            rows.append(row)

        # CSVに書き込み
        with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        return True

    except Exception as e:
        print(f"❌ 例外が発生しました: {e}")
        return False
