from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

URL = "https://danawa.com/?srsltid=AfmBOooQX8nBv8Dnfi5OLIemdJPi8Kizx-E9kD2iJkMNipkkLucg7zyX"


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초 까지 기다린다.

driver.get(URL)


search = driver.find_element(By.CSS_SELECTOR, '#AKCSearch')
search.send_keys('맥북프로')
submit = driver.find_element(By.CSS_SELECTOR, '.search__submit')
submit.send_keys(Keys.ENTER)

time.sleep(4)

products = driver.find_elements(By.CSS_SELECTOR, '.prod_item')

print(f"총 상품 개수: {len(products)}")
print(type(products))

for i, product in enumerate(products): # enumerate 인덱스와 그 인덱스의 값을 반환하는 함수.
  print(f"\n=== 상품{i + 1} ===")
  #상품 명
  try: 
    name = product.find_element(By.CSS_SELECTOR, '.prod_name').text
    print(f"상품명: {name}")
  except:
    print(f"상품명: 없음")

  # 가격
  try:
    prices = product.find_elements(By.CSS_SELECTOR, '.prod_pricelist > ul > li')
    for i, price in enumerate(prices):
      try:
        rowData = price.find_element(By.CSS_SELECTOR, '.price_sect > a > strong').text
        print(f"{i+1}번째 가격 - {rowData if rowData else '가격없음'}")
      except:
        print(f"{i+1}번째 가격 - 없음")
  except:
    print(f"상품 가격: 없음")

