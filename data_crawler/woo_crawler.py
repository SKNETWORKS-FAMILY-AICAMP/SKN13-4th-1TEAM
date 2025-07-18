import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://opengov.seoul.go.kr"
LIST_URL = f"{BASE_URL}/civilappeal/list"

def get_detail_content(detail_url):
    try:
        res = requests.get(detail_url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # 본문 영역 추출
        content_div = soup.select_one("div.comm-view-article.print-yes > div.line-all")
        if content_div:
            paragraphs = content_div.find_all("p")
            content_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
            return content_text
        else:
            return ""
    except Exception as e:
        print(f"에러 발생 상세 페이지 {detail_url}: {e}")
        return ""

def crawl_page(page_num):
    params = {"page": page_num}
    res = requests.get(LIST_URL, params=params)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("td.data-title.aLeft > a")
    results = []
    for a in rows:
        href = a.get("href")
        title = a.get_text(strip=True)
        # URL 조합
        detail_url = BASE_URL + href
        # id 추출 (/civilappeal/33929453 => 33929453)
        id_ = href.split("/")[-1]

        # 상세 페이지 본문 크롤링
        content = get_detail_content(detail_url)
        print(f"✅ {title}")

        results.append({
            "id": id_,
            "질문": title,
            "본문": content,
        })
        # time.sleep(0.3)  # 서버 부담 줄이기 위해 살짝 딜레이
    return results

def main():
    all_data = []
    MAX_PAGE = 2  # 원하는 크롤링 페이지 수 조절

    for page in range(1, MAX_PAGE + 1):
        print(f"크롤링 중: 페이지 {page}")
        page_data = crawl_page(page)
        all_data.extend(page_data)

    # CSV 저장
    with open("civilappeal_data.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "질문", "본문"])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"크롤링 완료, 총 {len(all_data)}건 저장됨.")

if __name__ == "__main__":
    main()
