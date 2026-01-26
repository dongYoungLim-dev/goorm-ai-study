from dotenv import load_dotenv # env 파일 읽기
import os 
import time
import json # python 의 자료형을 json 형태로 변환, 역변환 가능한 library 
'''
json Library의 dump(), dumps() 는 딕셔너리 파일을 json 데이터로 변환할때 아스키코드로 저장한다.
ensure_ascii=False 해당 옵션을 False 로 두고 사용하면 일반 텍스트 데이터로 저장한다.
indent=2 옵션을 주면 json 문자열을 출력할때 보기 좋게 정렬하여 추가 한다.
dump(), dumps() -> dictionary to json
load(), loads() -> json to dictionary
'''
import re # 정규 표현식 
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
# 비정형 텍스트를 JSON으로 변환하는 함수
# =====================================
def text_to_json(text, schema=None, strict_mode=True):
    """
    비정형 텍스트를 정형화된 JSON 데이터로 변환
    
    Args:
        text (str): 변환할 비정형 텍스트
        schema (dict, optional): 원하는 JSON 스키마 구조. None이면 자동 추론
        strict_mode (bool): True면 스키마를 엄격하게 따름, False면 유연하게 변환
    
    Returns:
        dict: 변환된 JSON 데이터
        또는 None: 변환 실패 시
    """
    # 스키마가 제공된 경우 스키마 정보를 프롬프트에 포함
    schema_section = ""
    if schema:
        schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
        schema_section = f"""
          [원하는 JSON 구조]
          다음 스키마에 맞춰 데이터를 변환해주세요:
          {schema_json}

        """
        if strict_mode:
            schema_section += "중요: 반드시 위 스키마 구조를 정확히 따라야 합니다. 추가 필드는 포함하지 마세요.\n"
        else:
            schema_section += "참고: 위 스키마를 참고하되, 텍스트에 있는 모든 유용한 정보를 포함해도 됩니다.\n"
    
    prompt = f"""
      [역할]
      전문 데이터 변환 전문가. 비정형 텍스트에서 구조화된 정보를 추출하여 JSON 형식으로 변환합니다.

      [규칙]
      1. 텍스트에서 명시적으로 언급된 정보만 추출합니다.
      2. 추측하거나 존재하지 않는 정보를 만들어내지 않습니다.
      3. 날짜, 숫자, 이름 등은 정확하게 추출합니다.
      4. JSON 형식은 유효한 형식이어야 합니다.
      5. 모든 문자열 값은 UTF-8로 인코딩 가능해야 합니다.

      {schema_section}[변환할 텍스트]
      {text}

      [출력 형식]
      반드시 유효한 JSON 형식으로만 출력하세요. 설명이나 추가 텍스트 없이 JSON만 출력합니다.
    """
    
    try:
        time.sleep(1)  # API 제한 고려
        
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
            print(f"에러: 응답이 생성되지 않았습니다. ({reason_text})")
            return None
        
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
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError as json_error:
            print(f"JSON 파싱 실패: {str(json_error)}")
            print(f"추출된 텍스트: {json_str[:200]}...")  # 처음 200자만 출력
            return None
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return None


def text_to_json_with_validation(text, schema=None, strict_mode=True):
    """
    비정형 텍스트를 JSON으로 변환하고 스키마 검증까지 수행
    
    Args:
        text (str): 변환할 비정형 텍스트
        schema (dict, optional): 검증할 JSON 스키마 구조
        strict_mode (bool): True면 스키마를 엄격하게 따름
    
    Returns:
        dict: {
            "success": bool,
            "data": dict or None,
            "errors": list,
            "warnings": list
        }
    """
    result = text_to_json(text, schema, strict_mode)
    
    if result is None:
        return {
            "success": False,
            "data": None,
            "errors": ["JSON 변환 실패"],
            "warnings": []
        }
    
    errors = []
    warnings = []
    
    # 스키마 검증
    if schema:
        # 필수 필드 확인
        if isinstance(schema, dict):
            for key in schema.keys():
                if key not in result:
                    if strict_mode:
                        errors.append(f"필수 필드 '{key}'가 누락되었습니다.")
                    else:
                        warnings.append(f"필드 '{key}'가 누락되었습니다.")
    
    return {
        "success": len(errors) == 0,
        "data": result,
        "errors": errors,
        "warnings": warnings
    }


# ==========================================
# 테스트 코드
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("비정형 텍스트 → JSON 변환기 테스트")
    print("=" * 60)
    
    # 테스트 케이스들
    test_cases = [
        {
            "name": "사용자 정보 추출",
            "text": """
            안녕하세요, 제 이름은 홍길동이고 나이는 30살입니다.
            이메일은 hong@example.com이고, 전화번호는 010-1234-5678입니다.
            서울시 강남구에 살고 있습니다.
            """,
            "schema": {
                "name": "이름",
                "age": "나이",
                "email": "이메일",
                "phone": "전화번호",
                "address": "주소"
            }
        },
        {
            "name": "상품 정보 추출",
            "text": """
            오늘 날씨가 정말 좋네요. 기온은 25도이고, 날씨는 맑습니다.
            습도는 60%이고, 바람은 약하게 불고 있습니다.
            """,
            "schema": {
                "temperature": "기온",
                "weather": "날씨",
                "humidity": "습도",
                "wind": "바람"
            }
        },
        {
            "name": "자동 추론 (스키마 없음)",
            "text": """
            회의 일정: 2024년 1월 25일 오후 2시
            장소: 서울시 강남구 테헤란로 123
            참석자: 김철수, 이영희, 박민수
            주제: 프로젝트 진행 상황 논의
            """,
            "schema": None
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"[테스트 {i}] {test_case['name']}")
        print(f"{'=' * 60}")
        
        print("\n[입력 텍스트]")
        print(test_case['text'].strip())
        
        if test_case['schema']:
            print("\n[원하는 스키마]")
            print(json.dumps(test_case['schema'], ensure_ascii=False, indent=2)) # dictionary 형을 json 현태로 변환 
        
        print("\n[변환 중...]")
        
        # 변환 실행
        if test_case['schema']:
            result = text_to_json_with_validation(
                test_case['text'], 
                test_case['schema'], 
                strict_mode=True
            )
            
            print("\n[변환 결과]")
            if result['success']:
                print("✓ 변환 성공!")
                print("\n[변환된 JSON]")
                print(json.dumps(result['data'], ensure_ascii=False, indent=2))
                
                if result['warnings']:
                    print("\n[경고]")
                    for warning in result['warnings']:
                        print(f"  - {warning}")
            else:
                print("✗ 변환 실패")
                print("\n[에러]")
                for error in result['errors']:
                    print(f"  - {error}")
                if result['data']:
                    print("\n[부분 변환 결과]")
                    print(json.dumps(result['data'], ensure_ascii=False, indent=2))
        else:
            result = text_to_json(test_case['text'])
            
            print("\n[변환 결과]")
            if result:
                print("✓ 변환 성공!")
                print("\n[변환된 JSON]")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("✗ 변환 실패")
        
        # API 제한 고려
        if i < len(test_cases):
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
