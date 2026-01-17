from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초 까지 기다린다.

url = "https://www.naver.com"
driver.get(url)

# 화면 크기 조정
driver.fullscreen_window() # 전체화면 모드로 변경
time.sleep(1)
driver.maximize_window() # 최대 창 크기로 변경
time.sleep(1)
driver.set_window_rect(100,100,500,500) # 특정 좌표(x,y)와 크기(width,height)로 변경
time.sleep(2)


print(driver.get_window_rect())

time.sleep(3)
driver.quit()
driver.set_window_position(0,0) # window 창을 position(0,0) 으로 이동
