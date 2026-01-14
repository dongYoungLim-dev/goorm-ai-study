import requests
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# .env 값을 가지고 오기 위해 load_dotenv 최초 1회 실행
load_dotenv()

response = requests.get("https://my-json-server.typicode.com/typicode/demo/posts")
print(response.json())


sendEmail = "ldy6740@naver.com"
recvEmail = "ldy6740@gmail.com"
password = os.environ.get('EMAIL_PW')

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

