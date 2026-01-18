# requests -> html 문서를 가져 올때 사용하는 패키지

import requests # html 문서 가져오는 패키지
from bs4 import BeautifulSoup as bs # html 문서의 형태를 잘 정리하여 다루기 쉬운 형태로 변환

url = 'https://k-digital.goorm.io/'

# url로 부터 html 자료를 받아온다.
response = requests.get(url)

if response.status_code == 200:
  # html 문서가 'html_txt'에 담긴다.
  html_txt = response.text

  # print(f'html_text = {html_txt}')
  html = bs(html_txt, 'html.parser')

  card = html.find_all('div', class_='card')

  for i, data in enumerate(card):
    title = data.find('div', class_='card-title').get_text()
    star = data.find('span', class_='_2KWt9f').get_text()
    print(f'{i+1}번째 - Title: {title}, Star: {star}')
else:
  print('연결 실패')