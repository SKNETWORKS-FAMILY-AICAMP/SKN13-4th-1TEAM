import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, version_main=138)

try:
    driver.get("https://eungdapso.seoul.go.kr/exp/pub/complaint_pub_lis.do")
    time.sleep(5)
    print("✅ 민원 리스트 접속 성공")
except Exception as e:
    print("❌ 접속 실패:", e)
finally:
    driver.quit()
