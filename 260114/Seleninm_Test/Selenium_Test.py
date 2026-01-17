from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

from dotenv import load_dotenv
import os
load_dotenv()

def main():
  # driver = webdriver.Chrome(ChromeDriverManager().install())
  service_obj = Service(ChromeDriverManager().install());
  option = Options()

  url = "https://k-digital.goorm.io/"
  option.add_experimental_option("detach", True);
  driver = webdriver.Chrome(service=service_obj, options=option)
  driver.get(url)

  driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div/div[2]/a[1]').click()
  driver.find_element(By.XPATH, '//*[@id="emailInput"]').send_keys('ldy6740@naver.com')
  driver.find_element(By.XPATH, '//*[@id="passwordInput"]').send_keys(os.environ.get('LOGIN_PW'))
  driver.find_element(By.XPATH, '//*[@id="app"]/section/div[4]/button').click()
  time.sleep(5)
  print(driver.page_source);
  # iframe = driver.find_element(By.TAG_NAME, "iframe")
  # driver.switch_to.frame(iframe)
  # driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div/div[2]/ul/div[1]/a/button').click()ㅋ
  # isDisabled = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[1]/button').get_attribute('disabled')
  # print(isDisabled)

  # driver.find_element(By.XPATH, '//*[@id="query"]').send_keys('맥북 프로')
  # driver.find_element(By.XPATH, '//*[@id="sform"]/fieldset/button').click()
  # products = driver.find_elements(By.CSS_SELECTOR, '.FHDg6Zu2._slog_visible')



if __name__ == '__main__':
  main()