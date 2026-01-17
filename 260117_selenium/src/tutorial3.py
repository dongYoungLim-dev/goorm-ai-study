from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초 까지 기다린다.

driver.get("https://www.naver.com")
driver.get('https://www.youtube.com/c/반원')
driver.get('https://www.google.com')

# 이전 창으로 2번 이동
driver.back()
driver.back()

# 다음 창으로 2번 이동
driver.forward()
driver.forward()

# 3초후 종료
time.sleep(3)
driver.quit()

