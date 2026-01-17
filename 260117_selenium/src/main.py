from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os
import time

load_dotenv()


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
driver.implicitly_wait(15)


# # =========================
# Danawa robots.txt
# SEO Optimization Version
# Updated: 2025-08-08
# =========================

# Global settings: Allow all major pages
# User-agent: *
# Disallow: /user_report/
# Disallow: /elec/Management
# Disallow: /my/
# Disallow: /member/
# Disallow: /error/
# Disallow: /404/
# Disallow: /*?iframe=*

# # Sitemap
# Sitemap: https://www.danawa.com/sitemap.xml

# 크롤링 대상(학습용)
URL = os.getenv('TARGET_URL')

driver.get(URL)
products = []
# append -> 리스트를 통체로 삽입 [1, 2, 3, [1, 2]], extend -> 리스트를 풀어서 삽입 [1, 2, 3, 1, 2]


search = driver.find_element(By.CSS_SELECTOR, '#AKCSearch')
search.send_keys('맥북')
submit = driver.find_element(By.CSS_SELECTOR, '.search__submit')
submit.send_keys(Keys.ENTER)
time.sleep(4)
# 페이지가 이동이 되면서 Web Element는 현재 페이지의 DOM과 연결이 되어있지만 페이지를 이동하는 액션으로 연결이 끊기게 된다.
for i in range(5):
  print(f"현재 {i + 1} 몇번째 ====================== ")

  product_count = driver.execute_script("return document.querySelectorAll('.prod_item').length")

  # products.extend(driver.find_elements(By.CSS_SELECTOR, '.prod_item'))
  items = driver.execute_script("""
    const items = document.querySelectorAll('.prod_item');
    const result = [];
    
    items.forEach((item, index) => {
        // 상품명 추출
        const nameEl = item.querySelector('.prod_name');
        const name = nameEl ? nameEl.innerText.trim() : '';
        
        // 가격 목록 추출
        const priceItems = item.querySelectorAll('.prod_pricelist > ul > li');
        const prices = [];
        
        priceItems.forEach((li, idx) => {
            const priceEl = li.querySelector('.price_sect > a > strong');
            const price = priceEl ? priceEl.innerText.trim() : '가격없음';
            prices.push(price || '가격없음');
        });
        
        if (name) {
            result.push({
                name: name,
                prices: prices
            });
        }
    });
    
    return result;
                                
  """)
  for product in items:
    products.append(product)
    
    # 결과 출력
    print(f"상품명: {product['name']}")
    for idx, price in enumerate(product['prices']):
        print(f"{idx+1}번째 가격 - {price}")
    print()


  time.sleep(2)
  # 2초뒤 다음 페이지로 이동
  paging = driver.find_element(By.CSS_SELECTOR, '.paging_edge_nav.paging_nav_next.click_log_page')
  paging.click()

time.sleep(5)
  


print(f'가져온 상품수는: {len(products)}')
# print(products[0][price])