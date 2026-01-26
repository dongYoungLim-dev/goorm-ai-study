from dotenv import load_dotenv # env 파일 읽기
import os 
import time
import json
import re
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
    
    # 응답 유효성 확인
    if not response.candidates or not response.candidates[0].content.parts:
      return f'에러 발생: 응답이 생성되지 않았습니다. (finish_reason: {response.candidates[0].finish_reason if response.candidates else "N/A"})'
    
    return response.text.strip() # strip -> 문자열 공백 제거
  except Exception as e:
    return f'에러 발생 {str(e)}'



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
    
    # 응답 유효성 확인
    if not response.candidates or not response.candidates[0].content.parts:
      finish_reason = response.candidates[0].finish_reason if response.candidates else "N/A"
      finish_reason_map = {
        0: "STOP (정상 완료)",
        1: "MAX_TOKENS (토큰 제한 도달)",
        2: "SAFETY (안전 필터 차단)",
        3: "RECITATION (재현 문제)",
        4: "OTHER (기타)"
      }
      reason_text = finish_reason_map.get(finish_reason, f"알 수 없는 이유 ({finish_reason})")
      return {
        "averageScore": 0,
        "comment": f"응답 생성 실패: {reason_text}",
        "isPass": False
      }
    
    response_text = response.text.strip()
    
    # JSON 부분 추출 (마크다운 코드 블록 제거)
    # ```json ... ``` 또는 ``` ... ``` 형태 제거
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if json_match:
      json_str = json_match.group(1)
    else:
      # 코드 블록이 없으면 중괄호로 감싸진 부분 찾기
      json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
      if json_match:
        json_str = json_match.group(0)
      else:
        json_str = response_text
    
    # JSON 파싱
    try:
      evaluation_result = json.loads(json_str)
      return evaluation_result
    except json.JSONDecodeError as json_error:
      # JSON 파싱 실패 시 기본값 반환
      return {
        "averageScore": 0,
        "comment": f"JSON 파싱 실패: {str(json_error)}",
        "isPass": False
      }
      
  except Exception as e:
    print(f"error: {e}")
    return {
      "averageScore": 0,
      "comment": f"평가 중 에러 발생: {str(e)}",
      "isPass": False
    }


# ==========================================
# TODO: 통합 실행 함수
# ==========================================
def evaluate_question(user_input):
  """
  사용자 질문을 받아 답변을 생성하고 평가하는 통합 함수
  
  Args:
    user_input (str): 사용자의 질문
    
  Returns:
    dict: {
      "question": 질문,
      "answer": 답변,
      "evaluation": 평가 결과 (averageScore, comment, isPass)
    }
  """
  # 1단계: 질문에 대한 답변 생성
  answer = user_question(user_input)
  
  # 2단계: 답변 평가
  evaluation = evaluation_bot(user_input, answer)
  
  # 3단계: 결과 반환
  return {
    "question": user_input,
    "answer": answer,
    "evaluation": evaluation
  }


# ==========================================
# 테스트 코드
# ==========================================
if __name__ == "__main__":
  print("=" * 60)
  print("AI 심사위원 시스템 테스트")
  print("=" * 60)
  
  # 샘플 질문들
  test_questions = [
    "Python에서 리스트와 튜플의 차이점은?",
    "비동기 프로그래밍이란?"
  ]
  
  # 첫 번째 질문으로 테스트
  test_question = test_questions[0]
  print(f"\n[테스트 질문] {test_question}\n")
  print("처리 중... (약 2-3초 소요)\n")
  
  try:
    # 통합 함수 실행
    result = evaluate_question(test_question)
    
    # 결과 출력
    print("-" * 60)
    print("[질문]")
    print(result["question"])
    print("\n[답변]")
    print(result["answer"])
    print("\n[평가 결과]")
    print(f"평균 점수: {result['evaluation'].get('averageScore', 'N/A')}")
    print(f"통과 여부: {result['evaluation'].get('isPass', 'N/A')}")
    print(f"코멘트: {result['evaluation'].get('comment', 'N/A')}")
    print("-" * 60)
    
    # JSON 형태로도 출력 (선택사항)
    print("\n[전체 결과 (JSON 형태)]")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
  except Exception as e:
    print(f"\n❌ 테스트 중 에러 발생: {str(e)}")
    import traceback
    traceback.print_exc()
  
  print("\n" + "=" * 60)
  print("테스트 완료")
  print("=" * 60)
