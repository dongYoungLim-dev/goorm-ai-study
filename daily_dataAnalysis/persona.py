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
# 기본 캐릭터 설정
# =====================================
DEFAULT_PERSONA = {
    "role": "Python 언어를 이용한 15년차 개발자, 후배들에게 지식 공유를 좋아한다.",
    "background": "사내 서비스 개발, 막 입사한 주니어 개발자의 질문",
    "rules": [
        "사실에 근거하여 답변한다.",
        "후배 개발자지만 반말은 지양한다.",
        "지식에 대한 답변은 비유와 함께 작성해준다.",
        "항상 일관된 캐릭터를 유지한다.",
        "이전 대화 내용을 기억하고 자연스럽게 연결한다."
    ]
}


# =====================================
# PersonaChatbot 클래스
# =====================================
class PersonaChatbot:
    """
    절대 캐릭터를 붕괴시키지 않는 페르소나 챗봇
    
    대화 히스토리를 관리하며 일관된 캐릭터를 유지합니다.
    """
    
    def __init__(self, persona=None, model=None):
        """
        초기화
        
        Args:
            persona (dict): 캐릭터 설정. None이면 기본 캐릭터 사용
            model: Gemini 모델. None이면 기본 모델 사용
        """
        self.persona = persona if persona else DEFAULT_PERSONA.copy()
        self.model = model if model else genai.GenerativeModel('gemini-3-flash-preview')
        self.history = []  # 대화 히스토리: [{"role": "user"/"assistant", "content": "..."}]
    
    def _build_prompt(self, user_input):
        """
        프롬프트 생성 (캐릭터 정보 + 대화 히스토리 + 현재 질문)
        
        Args:
            user_input (str): 사용자 입력
            
        Returns:
            str: 완성된 프롬프트
        """
        # 캐릭터 설정 부분
        persona_section = f"""
          [역할]
          {self.persona['role']}

          [배경]
          {self.persona['background']}

          [규칙]
        """
        for i, rule in enumerate(self.persona['rules'], 1):
            persona_section += f"{i}. {rule}\n"
        
        # 대화 히스토리 부분
        history_section = ""
        if self.history:
            history_section = "\n[대화 히스토리]\n"
            for msg in self.history:
                role_name = "사용자" if msg['role'] == 'user' else "챗봇"
                history_section += f"{role_name}: {msg['content']}\n"
        
        # 현재 대화 부분
        current_section = f"""
          [현재 대화]
          사용자: {user_input}
        """
        
        # 전체 프롬프트 조합
        prompt = persona_section + history_section + current_section
        
        return prompt
    
    def chat(self, user_input):
        """
        사용자 입력에 대해 응답 생성
        
        Args:
            user_input (str): 사용자 입력
            
        Returns:
            str: 챗봇 응답
        """
        try:
            time.sleep(1)  # API 제한 고려
            
            # 프롬프트 생성
            prompt = self._build_prompt(user_input)
            
            # API 호출
            response = self.model.generate_content(prompt)
            
            # 응답 유효성 확인
            if not response.candidates or not response.candidates[0].content.parts:
                finish_reason = response.candidates[0].finish_reason if response.candidates else "N/A"
                error_msg = f'에러 발생: 응답이 생성되지 않았습니다. (finish_reason: {finish_reason})'
                # 히스토리에 사용자 입력만 추가
                self.history.append({"role": "user", "content": user_input})
                return error_msg
            
            # 응답 추출
            assistant_response = response.text.strip()
            
            # 히스토리에 추가
            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            error_msg = f'에러 발생: {str(e)}'
            # 에러 발생 시에도 사용자 입력은 히스토리에 추가
            if not any(msg['role'] == 'user' and msg['content'] == user_input for msg in self.history):
                self.history.append({"role": "user", "content": user_input})
            return error_msg
    
# ==========================================
# 테스트 코드
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("페르소나 챗봇 테스트")
    print("=" * 60)
    
    # 챗봇 인스턴스 생성
    chatbot = PersonaChatbot()
    
    # 테스트 대화들
    test_conversations = [
        "안녕하세요! 처음 뵙겠습니다.",
        "Python에서 리스트와 튜플의 차이점이 뭔가요?",
        "아까 말씀하신 내용 중에서, 튜플을 언제 사용하면 좋을까요?",
        "제 이름은 김철수입니다. 앞으로 잘 부탁드립니다."
    ]
    
    print("\n[테스트 시작]")
    print("여러 대화를 거쳐도 캐릭터가 일관되게 유지되는지 확인합니다.\n")
    
    try:
        for i, user_input in enumerate(test_conversations, 1):
            print(f"\n{'=' * 60}")
            print(f"[대화 {i}]")
            print(f"사용자: {user_input}")
            print(f"\n처리 중...")
            
            response = chatbot.chat(user_input)
            
            print(f"\n챗봇: {response}")
            print(f"{'=' * 60}")
            
            # API 제한 고려
            if i < len(test_conversations):
                time.sleep(1)
        
        # 대화 히스토리 출력
        print("\n")
        chatbot.print_history()
        
        # 캐릭터 일관성 확인
        print("\n[캐릭터 일관성 확인]")
        print("대화 히스토리를 확인하여 캐릭터가 일관되게 유지되었는지 검증합니다.")
        print(f"총 대화 수: {len(chatbot.history)}개")
        
    except Exception as e:
        print(f"\n❌ 테스트 중 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)
