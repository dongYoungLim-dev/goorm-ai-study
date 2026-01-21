# 객체지향 설계원칙 - OCP(Open-Closed Principle)
# 기능 확장은 가능하지만 기능 수정을 막는 원칙
# 개념적으로 OCP 원칙을 적용 여부에 대한 판단은 기능이 확장을 많이 필요한지 판단하고 원칙을 적용할지 결정해야 한다.

# 배보다 배꼽이 더 큰 상황이 될 수 있다.

# OCP 원칙 X
class Message:
  # message 추상 클래스
  def __init__(self, data):
    self.data = data

class FirstGrademessage(Message):
  # FirstGrade에 대한 메세지 처리 클래스
  pass
class SecondGradeMessage(Message):
  # SecondGrade에 대한 메세지 처리 클래스
  pass
class ThirdGradeMessage(Message):
  # ThirdGrade에 대한 메세지 처리 클래스
  pass
class DefaultGradeMessage(Message):
  # DefaultGrade에 대한 메세지 처리 클래스
  pass

# Grade에 따라 elif 조건문을 추가하여 필요 동작을 추가한다. 결국 클래스 내부 메소드 수정과, 새로운 클래스를 추가 해야 한다.
# 이러면 OCP 원칙이 위배 된다.
class GradMessageClassification():
  # Grade에 따른 메세지 분류 클래스
  def __init__(self, data):
    self.data = data
  
  def classification(self):
    if (self.data['grade'] == 1):
      return FirstGrademessage(self.data)
    elif (self.data['grade'] == 2):
      return SecondGradeMessage(self.data)
    elif (self.data['grade'] == 3):
      return ThirdGradeMessage(self.data)
    else:
      return DefaultGradeMessage(self.data)


# OCP 원칙 O
class Message:
  # message 추상 클래스
  def __init__(self, data):
    self.data = data

  @staticmethod # 클래스와 관련은 있지만 인스턴스 상태가 필요 없는 함수에 적합합니다. // 인스턴스를 생성하지 않고 해당 클래스의 메소드를 호출이 필요한 경우에 사용됩니다. Message.is_collect_grade_message() 와 같이 사용됩니다.
  def is_collect_grade_message(data: dict):
    return False

class FirstGradeMessage(Message):
  # FirstGrade에 대한 메세지 처리 클래스
  @staticmethod
  def is_collect_grade_message(data: dict):
    return data['grade'] == 1

class SecondGradeMessage(Message):
  # SecondGrade에 대한 메세지 처리 클래스
  @staticmethod
  def is_collect_grade_message(data: dict):
    return data['grade'] == 2

class ThirdGradeMessage(Message):
  # ThirdGrade에 대한 메세지 처리 클래스
  @staticmethod
  def is_collect_grade_message(data: dict):
    return data['grade'] == 3

class DefaultGradeMessage(Message):
  # DefaultGrade에 대한 메세지 처리 클래스
  pass

# GradeMessageClassification 클래스는 grade가 추가되어도 수정되지 않는다. 기능 추가가 필요하면 Message 클래스를 상속받아 새로운 클래스를 추가하면 된다.
class GradeMessageClassification():
  # Grade에 따른 메세지 분류 클래스
  def __init__(self, data):
    self.data = data

  def classification(self):
    for grade_message_cls in Message.__subclasses__(): # __subclasses__() 메소드는 클래스를 상속받는 자식 클래스를 리스트로 반환한다.
      try:
        if grade_message_cls.is_collect_grade_message(self.data):
          return grade_message_cls(self.data)
      except KeyError:
        continue
      
      return DefaultGradeMessage(self.data)