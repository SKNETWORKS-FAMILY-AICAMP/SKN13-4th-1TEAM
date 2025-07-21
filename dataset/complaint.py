from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# 설정
CHROMEDRIVER_PATH = r"C:\Aicamp\chromedriver-win64\chromedriver-win64\chromedriver.exe"
LIST_URL = "https://eungdapso.seoul.go.kr/exp/pub/complaint_pub_lis.do"
MAX_PAGE = 28  # 수집할 페이지 수
SAVE_PATH = "complaint_data.csv"


# Selenium 드라이버 설정
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0")
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

# 결과 저장 리스트
data = []


try:
    driver.get(LIST_URL)
    print("✅ 민원 리스트 접속 성공")

    current_group = 1

    for page in range(1, MAX_PAGE + 1):
        try:
            if page > 1:
                # 5단위 그룹 넘기기
                if (page - 1) % 5 == 0:
                    next_btn = driver.find_element(By.CSS_SELECTOR, "#content > div.subcont_contwrap > div.data_paing_wrap > a.next_go")
                    next_btn.click()
                    time.sleep(1.5)

                # 해당 페이지 번호 클릭
                page_btn = driver.find_element(By.LINK_TEXT, str(page))
                page_btn.click()
                time.sleep(1.5)

            # 민원 항목 수집
            items = driver.find_elements(By.CSS_SELECTOR, ".rp_inlink")

            for idx in range(len(items)):
                items = driver.find_elements(By.CSS_SELECTOR, ".rp_inlink")
                item = items[idx]
                title = item.text
                item.click()
                time.sleep(1.5)

                soup = BeautifulSoup(driver.page_source, "html.parser")
                question = soup.select_one(
                    "#content .board_viewer_contbox > div > p:nth-child(2)"
                )
                answer = soup.select_one(
                    "#content .res_hcell.restd > div"
                )

                if question and answer:
                    data.append({
                        "id": len(data) + 1,
                        "질문": question.get_text(strip=True),
                        "본문": answer.get_text(" ", strip=True)
                    })

                driver.back()
                time.sleep(1.5)

        except Exception as e:
            print(f"❌ 페이지 로딩 실패 (page {page}): {e}")
            continue

except Exception as e:
    print(f"❌ 전체 크롤링 오류: {e}")

finally:
    driver.quit()

# 저장
df = pd.DataFrame(data)
df.to_csv(SAVE_PATH, index=False, encoding="utf-8-sig")
print(f"\n✅ 크롤링 완료: 총 {len(df)}건 → {SAVE_PATH} 저장됨")
