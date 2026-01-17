from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초 까지 기다린다.

url = "https://www.naver.com"
driver.get(url)

search = driver.find_element(By.CSS_SELECTOR, '#query')
search.send_keys('고슴도치')
search.send_keys(Keys.ENTER)
time.sleep(2)


posts = driver.find_element(By.XPATH, '//*[@id="fdr-659511c3d1644c6c9702b7cffd8d734a"]/div/div/div/div/div[1]/div[2]/div[1]/a') # 렌더링 과정에서 해당 xpath 값을 찾지 못해서 안됨
posts[0].click()
time.sleep(2)