import requests
from bs4 import BeautifulSoup
import csv
import os
import time


def build_monthly_url(prec_no, block_no, year):
    return (
        f"https://www.data.jma.go.jp/stats/etrn/view/monthly_s1.php?"
        f"prec_no={prec_no}&block_no={block_no}&year={year}&view=p1"
    )


def fetch_monthly_temperature(prec_no, block_no, year, user_agent="Mozilla/5.0"):
    url = build_monthly_url(prec_no, block_no, year)
    print(f"📄 Fetching: {url}")

    headers = {"User-Agent": user_agent}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Error: status {resp.status_code}")
        return None

    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.select_one("table.data2_s")
    if not table:
        print("❌ Table not found")
        return None

    rows = table.select("tr")
    result = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 8 and cells[0].text.strip().isdigit():
            month = int(cells[0].text.strip())
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
    locations = {
        "tokyo": ("44", "47662"),
        "sapporo": ("14", "47412"),
        "naha": ("91", "47936"),
    }
    years = range(1920, 2024)
    delay_seconds = 1.5

    for city, (prec_no, block_no) in locations.items():
        all_data = []
        for year in years:
            yearly_data = fetch_monthly_temperature(prec_no, block_no, year)
            if yearly_data:
                all_data.extend(yearly_data)
            time.sleep(delay_seconds)  # 💤 polite delay
        save_to_csv(all_data, f"data/{city}_monthly_avg_temp.csv")
        print(f"✅ Saved: data/{city}_monthly_avg_temp.csv")
