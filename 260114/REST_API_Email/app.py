import requests # RESTful API 사용 Library
import smtplib # 메일 발송 Library
from email.mime.text import MIMEText # 메일의 body의 내용을 작성하기 위한 Library
# 이메일은 Multipurpose Internet Mail Extensions 이라는 표준 형식에 맞게 작성을 해야 하는데 이를 도와준다.

from dotenv import load_dotenv # env 파일을 읽어 오는 라이브러리
import os # 파일 생성, 폴더 탐색, 환경 변수 읽기 위에 os와 소통하는 Library

# .env 값을 가지고 오기 위해 load_dotenv 최초 1회 실행
load_dotenv()

response = requests.get("https://my-json-server.typicode.com/typicode/demo/posts")
print(response.json())


sendEmail = "ldy6740@naver.com"
recvEmail = "ldy6740@gmail.com"
password = os.environ.get('EMAIL_PW') # .env 파일에 있는 'EMAIL_PW' 내용으로 치환된다. 

smtpName = "smtp.naver.com"
smtpPort = "587"


text = "테스트 메일입니다. 지금 파이썬으로 작성하고 있습니다.222222"
msg = MIMEText(text, _charset = "utf-8")

msg["Subject"] = "테스트 메일 제목 Python 개발222222"
msg["From"] = sendEmail
msg['To'] = recvEmail
print(msg.as_string())

s = smtplib.SMTP(smtpName, smtpPort)
s.starttls() # TLS 보안 처리 
s.login(sendEmail, password)
s.sendmail(sendEmail, recvEmail, msg.as_string()) 
s.close()

