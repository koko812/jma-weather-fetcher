import requests
from bs4 import BeautifulSoup
import csv
import os

def build_monthly_url(prec_no, block_no, year):
    return (
        f"https://www.data.jma.go.jp/stats/etrn/view/monthly_s1.php?"
        f"prec_no={prec_no}&block_no={block_no}&year={year}&view=p1"
    )

def fetch_monthly_temperature(prec_no, block_no, year):
    url = build_monthly_url(prec_no, block_no, year)
    print(f"📄 取得中: {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"❌ エラー: status {resp.status_code}")
        return None

    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.select_one("table.data2_s")
    if not table:
        print("❌ データテーブルが見つかりません")
        return None

    rows = table.select("tr")
    result = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2 and cells[0].text.strip().isdigit():
            month = int(cells[0].text.strip())
            # 修正後（平均気温は5列目 = index 4）
            # 修正後（7列目：平均気温）
        if len(cells) >= 8:
            avg_temp = cells[7].text.strip()
            try:
                avg_temp = float(avg_temp)
            except ValueError:
                avg_temp = None
            result.append({"year": year, "month": month, "avg_temp": avg_temp})
    return result

def save_to_csv(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "month", "avg_temp"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    prec_no = "44"      # 東京都
    block_no = "47662"  # 東京（千代田区）
    years = range(1925, 2024)

    all_data = []
    for year in years:
        yearly_data = fetch_monthly_temperature(prec_no, block_no, year)
        if yearly_data:
            all_data.extend(yearly_data)

    save_to_csv(all_data, "data/tokyo_monthly_avg_temp.csv")
    print("✅ 保存完了: data/tokyo_monthly_avg_temp.csv")
