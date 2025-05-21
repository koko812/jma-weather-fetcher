import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.data.jma.go.jp"


def build_html_url(prec_no, block_no, date):
    y, m, d = date.split("-")
    return (
        f"{BASE_URL}/stats/etrn/view/hourly_s1.php?"
        f"prec_no={prec_no}&block_no={block_no}&year={y}&month={int(m)}&day={int(d)}&view="
    )


BASE_URL = "https://www.data.jma.go.jp"

def extract_csv_url(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # <a href=...dl.php> にマッチ
    a_link = soup.select_one('a[href*="dl.php"]')
    if a_link:
        return urljoin(BASE_URL, a_link["href"])

    # <form action=...dl.php> にマッチ
    form = soup.select_one('form[action*="dl.php"]')
    if form:
        return urljoin(BASE_URL, form["action"])

    return None


def extract_csv_form_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    form = soup.select_one('form[action*="dl.php"]')
    if not form:
        return None, None

    action_url = urljoin(BASE_URL, form["action"])
    inputs = form.find_all("input")
    data = {inp["name"]: inp.get("value", "") for inp in inputs if inp.has_attr("name")}

    return action_url, data


def fetch_jma_csv(prec_no, block_no, date, output_html_path=None, output_csv_path=None):
    html_url = build_html_url(prec_no, block_no, date)
    print(f"📄 HTMLページ取得中: {html_url}")
    html_resp = requests.get(html_url)

    if output_html_path:
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_resp.text)

    if html_resp.status_code != 200:
        print(f"❌ HTML取得失敗: status {html_resp.status_code}")
        return False

    csv_url = extract_csv_url(html_resp.text)
    if not csv_url:
        print("❌ CSVフォームが見つかりませんでした")
        return False

    print(f"📡 CSVリンク取得: {csv_url}")
    if output_csv_path:
        csv_resp = requests.get(csv_url)
        if csv_resp.status_code == 200:
            os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
            with open(output_csv_path, "wb") as f:
                f.write(csv_resp.content)
            print(f"✅ 保存しました: {output_csv_path}")
        else:
            print(f"❌ CSV取得失敗: status {csv_resp.status_code}")
            return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prec", required=True, help="都道府県番号（例：44=東京）")
    parser.add_argument("--block", required=True, help="地点番号（例：47662）")
    parser.add_argument("--date", required=True, help="日付 (YYYY-MM-DD)")
    parser.add_argument("--output", required=True, help="CSVの出力先パス")
    args = parser.parse_args()

    fetch_jma_csv(args.prec, args.block, args.date, args.output)
