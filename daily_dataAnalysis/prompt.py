from dotenv import load_dotenv # env 파일 읽기
import os 
import time
import google.generativeai as genai # gemini api 연동 Library


load_dotenv()


# Gemini Library Setting
genai.configure(api_key=os.getenv('GEMINI_API_KEY')) # API KEY 연결

# 모델 초기화 - Gemini 3 Flash Preview (무료 티어 최적)
# ==================
# 무료 버전 일이 사용 제한
# RPM(분당 API 요청 건수) - 5건
# TPM(분당 토큰 수) - 250k
# RPD(하루 API 요청 건수) - 20건
model = genai.GenerativeModel('gemini-3-flash-preview')

# =====================================
# TODO: 사용자 질문 함수 작성
# =====================================

def user_question(input):
  # 사용자 Prompt 정의
  prompt = f"""
  [역할]
  Python 언어를 이용한 15년차 개발자, 후배들에게 지식 공유를 좋아한다.
  
  [배경]
  사내 서비스 개발, 막 입사한 주니어 개발자의 질문

  [규칙]
  1. 사실에 근거하여 답변한다.
  2. 후배 개발자 지만 반말은 지양한다.
  3. 지식에 대한 답변은 비유와 함께 작성해준다.
  
  [질문]
  {input}
  """

  try:
    time.sleep(1) # 
    response = model.generate_content(prompt)
    return response.text.strip() # strip -> 문자열 공백 제거
  except Exception as e:
    return f'에러 발생 {str(e)}'


# 함수 테스트
# user_input = input('질문을 입력해주세요 : ')
# answer = user_question(user_input)

# print(answer)

# ==========================================
# TODO: 받은 질문 평가하기
# ==========================================
def evaluation_bot(user_input, answer):
  prompt = f"""
  [역할]
  전달한 질문과 답변을 평가하는 전문 평가사
  아래 기준을 이용하여 답변에 대한 점수 부여

  [평가기준]
  1. 정확성 (0 - 10점)
  2. 명확성 (0 - 10점)
  3. 친절한가 (0 - 10점)
  4. 평균 점수가 5점 보다 높으면 "Pass", 낮으면 "Fail"
  
  [출력형식=JSON] 
  {{"averageScore": 평균점수, "comment": 코멘트, "isPass": 통과여부 }}
  

  [평가 내용]
  질문 : {user_input}
  답변 : {answer}
  """

  try:
    time.sleep(1)
    response = model.generate_content(prompt)
    return response.text.strip()
  except Exception as e:
    print(f"error: {e}");

# TODO: 반환된 답변에서 JSON 부분만 추출 방법
