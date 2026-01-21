import json
import requests;

class OrderProcessor:
  def process_order(self, order_id, items, user_email):
    # 1. [비즈니스 로직] 가격 및 세급 계산 (기획팀 / 재무팀 관할)
    total_price = 0
    for item in items: 
      price = items['price'] * item['quantity']
      if item['category'] == 'electronice':
        price *= 0.9 # 전자제품 10% 할인  
      total_price += price

    tax = total_price * 0.1 # 
    final_amount = total_price + tax
    print(f"계산완료: 총액 {final_amount}")


    # 2. [인프라 로직] 주문 정보를 DB(여기선 파일) 에 저장 (DBA/개발팀 관할)
    order_data = {
      'order_id': order_id,
      'amount': final_amount,
      'status': 'PAID'
    }
    
    try:
      with open(f"order_{order_id}.json", "w") as f:
        json.dump(order_data, f)
      print(f"DB 저장 완료")
    except IOError as e:
      print(f"DB 에러: {e}")
      return

    # 3. [프로젠테이션 로직] 고객에게 이메일 발송 (마케팅/디자인팀 관할)
    email_content = f"<h1>주문 감사합니다.! </h1><p>결제금액: {final_amount}</p>"
    print(f"이메일 전송 to {user_email} : {email_content}")


"""
위 코드 SRP 규칙에 위배되는 코드이다. 주문프로 세스와 연과
"""
# 로그인 과정에서 
# 첫번재 규칙 SRP 를 위해 클래스 내부 메소드를 외부 클래스로 분리하는 방법에 대한 정의
# 클래스에게 부여한 책임, 역할이 무엇이냐에따라 내부에 속하냐 외부에 속하냐가 달라진다.
# 전체 로그인 프로그램에서 로그인의 흐름을 관리한다. 라는 역할을 부여 했다면, 
# 로그인 흐름과 연관이 있는 메소드를 내부에 두고
# 외부에서 필요한 로직을 가지고 와서 사용한다. 

# LoginController 클래스는 로그인 프로그램의 전체 흐름을 담당한다.
class LoginControl
class router:
  def navigate_to_home(self):
    print("메인 페이지로 이동")

class view:
  def show_error(self, message):
    print(f"오류 메시지: {message}")
  def show_spinner(self):
    print("로딩 스피너 표시")
  def hide_spinner(self):
    print("로딩 스피너 숨기기")
  def enable_btn(self):
    print("버튼 활성화")
  def disable_btn(self):
    print("버튼 비활성화")
  def show_alert(self, message):
    print(f"알림 메시지: {message}")

class NetworkError(Exception):
  pass

class LoginController:
  def __init__(self):
    self.user_inspection = userInspection()
  # LoginController 클래스의 역할과 연관리 없는 기능을 외부 클래스로 분리한다.
  def __init__(self, user_inspection, validator, router, view):
    self.user_inspection = user_inspection # 서버에 요청 하여 회원 유무를 판단.
    self.validator = validator # 로그인 입력값이 유효성에 맞는지 체크
    self.router = router # 회원 유무 통과, 유효성 통과 되면 로그인이 되고 메인 페이지로 이동
    self.view = view # 로그인 입력값이 유효성을 통과 못하면 화면에 알려주는 역할
  
  # 화면에서 로그인 버튼을 클릭하면 실행이 되는 메소드 (로그인 프로그램 시작 지점)
  def on_login_btn_clicked(self, userId, userPw):
    self._set_loading(True)
    try:
      self._process_login(userId, userPw) # 로그인 프로그램 시작, 입력값 전달
    except Exception as e:
      self._handle_error(e)
    finally:
      # 성공 실패 여부와 상관없이 로딩 상태 초기화
      self._set_loading(False)

  # 로그인 프로그램 전체 흐름 제어
  def _process_login(self, userId, userPw):
    # 입력값 유효성 체크 결과와 통과를 하지 못했다면 에러 메시지 반환 후 종료
    is_valid, err_msg = self.validator.validate_input(userId, userPw)
    if not is_valid:
      self.view.show_error(err_msg) # 유효성 검사 통과 못하면, 화면에 메시지 표시
      return # 통과하지 못했다면 다름 로직 실행 하지않고 종료
    
    isUser, resultMsg = self.user_inspection.fatchApi(userId, userPw) # 서버에서 회원 정보 판단 결과와 msg 반환

    if isUser:
      self.router.navigate_to_home() # 회원정보가 있으면 로그인 성공, 메인 페이지 이동
    else:
      self.view.show_error(resultMsg)

  # 로딩 상태 처리 LoginController 클래스에 흐름과 연관리 있는 메소드 이기 때문에 내부에 둔다.
  def _set_loading(self, is_loading):
    if is_loading:
      # 화면에 로딩중 표시.
      self.view.show_spinner() # 화면에 로딩 스피너 표시
      self.view.disable_btn() # 화면 버튼 비활성화
    else:
      # 다음을 진행한다.
      self.view.hide_spinner() # 화면에 로딩 스피너 숨기기
      self.view.enable_btn() # 화면 버튼 활성화
  
  # 오류 처리 메소드도 프로그램 진행에서 발생하는 오류를 처리하는 메소드, 흐름과 연관이 있기 때문에 내부에 둔다.
  def _handle_error(self, error):
    print(f"오류 발생 {error}") # 로그 남기기, print로 했지만 파일에 기록하여 특정 디렉토리에 파일 저장

    if isinstance(error, NetworkError):
      self.view.show_alert('네트워크 오류가 발생했습니다. 다시 시도해주세요.')
    else:
      self.view.show_alert('알 수 없는 오류가 발생했습니다. 다시 시도해주세요.')


# LoginController 역할 관점에서 연관이 없는 기능을 따로 분리하여 클래스로 만든다.

class userInspection:
  def fatchApi(self, userId, userPw):
    url = "api url"
    response = requests.get(url)
    if response.status_code == 200:
      return True, "로그인 성공"
    else:
      return False, "로그인 실패"
      
class validator:
  def validate_input(self, userId, userPw):
    if len(userId) < 3 or len(userPw) < 8:
      return False, "아이디와 비밀번호는 3자 이상이어야 합니다."
    return True, "유효성 검사 통과"

class router:
  def navigate_to_home(self):
    print("메인 페이지로 이동")

class view:
  def show_error(self, message):
    print(f"오류 메시지: {message}")
  def show_spinner(self):
    print("로딩 스피너 표시")
  def hide_spinner(self):
    print("로딩 스피너 숨기기")
  def enable_btn(self):
    print("버튼 활성화")
  def disable_btn(self):
    print("버튼 비활성화")
  def show_alert(self, message):
    print(f"알림 메시지: {message}")


controller = LoginController(userInspection(), validator(), router(), view())
controller.on_login_btn_clicked("test", "test") # 로그인 버튼을 클릭하면 로그인 프로그램 시작


"""
- SRP는 객체에게 주어진 역할에 위배되는 행동을 담지 않는다.

위배되는 행동이라고 객체 내부의 데이터를 사용하여야 진행이 된다면 따로 분리하지 않아고 된다.

- SRP는 치킨을 파는 가게라는 가정을 하면

사람 1. 사장 역할

사람 2. 배달 역할

사람 3. 닭 손질 역할

사람 4. 닭 튀김 역할

이라고 하면 사장이 주문을 받아야 하는데 배달을 가면 장사를 멈춘다. (프로그램이 멈춘다.)

배달 역할이 닭 손질까지 하면 손질중에는 배달을 못간다. (다음 프로그램으로 진행이 안된다.)

닭 손질 역할이 닭을 튀기면 닭 손질 로직이 멈추기 때문에 닭 튀김을 할 수없다. (프로그램이 느려진다.)

- SRP 는 역할에 대한 수정만 받아야 한다.
"""