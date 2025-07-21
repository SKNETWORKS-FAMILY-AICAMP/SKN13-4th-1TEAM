import os
import time
import requests
import fitz  # PyMuPDF
import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ▶ 설정
# CHROMEDRIVER_PATH = r"C:\Aicamp\chromedriver-win64\chromedriver-win64\chromedriver.exe"
BASE_URL = "https://opengov.seoul.go.kr"
SAVE_PATH = "press_crawled.csv"

# ▶ 셀레니움 드라이버 설정
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0")
# options.add_argument("--headless")  # 필요 시 사용

# driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

data = []
article_id = 1

# 크롤링할 페이지 범위 정하기
num_start = 1
num_end = 3
for i in range(num_start, num_end + 1):
    page_url = f"{BASE_URL}/press/list?page={i}"
    print(f"✅ 리스트 접속 성공: {i}페이지")
    driver.get(page_url)
    time.sleep(1)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr td.data-title.aLeft > a")))
        elements = driver.find_elements(By.CSS_SELECTOR, "table tbody tr td.data-title.aLeft > a")
        detail_links = [el.get_attribute("href") for el in elements]
        print(f"📌 상세페이지 링크 수: {len(detail_links)}개")

        for link in detail_links:
            try:
                driver.get(link)
                time.sleep(1.5)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                # 제목 수집
                title_tag = soup.select_one("#content > div > div.view-content.view-content-article > h3")
                if not title_tag:
                    print("❌ 제목 없음, 스킵")
                    continue
                title = title_tag.get_text(strip=True)

                # PDF 링크 수집
                pdf_tag = soup.select_one("#content > div > div.view-content.view-content-article a[href$='.pdf']")
                if pdf_tag:
                    href = pdf_tag.get("href")
                    if isinstance(href, str):
                        pdf_url = BASE_URL + href
                        print(f"🔎 상세페이지: {link}")
                        print(f"👉 제목: {title}")
                        print(f"👉 PDF 링크: {pdf_url}")
                    else:
                        print(f"❌ PDF href 오류: {title} / {link}")
                        continue
                else:
                    pdf_tag = soup.select_one("#content > div > div.view-content.view-content-article > div:nth-child(8) > ul > li:nth-child(1) > span > a:nth-child(2) > i")
                    if pdf_tag:
                        href = pdf_tag.get("href")
                        if isinstance(href, str):
                            pdf_url = BASE_URL + href
                            print(f"🔎 상세페이지: {link}")
                            print(f"👉 제목: {title}")
                            print(f"👉 PDF 링크: {pdf_url}")
                        else:
                            print(f"❌ PDF href 오류: {title} / {link}")
                            continue
                    else:
                        print(f"❌ PDF 없음: {title} / {link}")
                        continue

                # PDF 요청 및 파싱
                res = requests.get(pdf_url)
                doc = fitz.open(stream=BytesIO(res.content), filetype="pdf")
                text = "\n".join([page.get_text() for page in doc])

                data.append({
                    "id": article_id,
                    "질문": title,
                    "본문": text.strip()
                })
                article_id += 1

            except Exception as e:
                print(f"❌ 상세페이지 처리 오류: {e}")
                continue

    except Exception as e:
        print(f"❌ 전체 크롤링 오류 (page {i}): {e}")
        continue

driver.quit()

# ▶ CSV 저장
df = pd.DataFrame(data)
df.to_csv(SAVE_PATH, index=False, encoding="utf-8-sig")
print(f"\n✅ 크롤링 완료: 총 {len(df)}건 수집 → {SAVE_PATH}")
