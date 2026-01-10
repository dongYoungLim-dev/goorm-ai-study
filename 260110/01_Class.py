# 왜 클래스가 필요한 이유 

# 함수로 계산 기능을 구현 하고, 서로 다른 값을 동시에 계산하고 싶으면?
result1 = 0
result2 = 0

def add1(num):
  global result1
  result1 += num
  return result1

print('계산기 1')
print(add1(2));
print(add1(4));

print('='*20)

def add2(num):
  global result2
  result2 += num
  return result2

print("계산기 2")
print(add2(2));
print(add2(5));


# 클래스로 계산기 구현, 클래스를 만들때 이름을 만드는 관례 이름은 대문자로 시작한다.
class Calculator:
  def __init__(self):
    self.result = 0

  def add(self, num):
    self.result += num
    return self.result
  
cal1 = Calculator()
cal2 = Calculator()

print('계산기 1')
print(cal1.add(2));
print(cal1.add(5));

print("=" * 20)

print('계산기 2')
print(cal2.add(4))
print(cal2.add(8))

# 함수로 계산기를 구현하면 동시에 다른 계산을 하고 싶으면 같은 기능을 하는 함수를 하나더 만들어서 사용해야 하는 비효율이 발생
# 클래스(붕어빵 틀)로 계산기를 구현하면 기능은 하나만 구현하고, 인스턴스 객체(붕어빵)만 여러개 만들어 동시에 다른 계산이 가능하다. 코드의 반복을 줄일 수 있다.


class FourCal:
  def setdata(self, first, second): # self(필수) -> 자기 자신을 의미 [클래스를 생성한 인스턴스를 담은 객채가 setdata함수가 실행이 될때 self에 담기게 된다]
    self.first = first
    self.second = second
  def add(self):
    result = self.first + self.second
    return result
  def mul(self):
    result = self.first * self.second
    return result
  def sub(self):
    result = self.first - self.second
    return result
  def div(self):
    result = self.first / self.second
    return result

# 객체 변수 
# 클래스 인스턴스를 생성하면 a 변수에 담으면, a 클래스 인스턴스를 담은 객체가 되고 클래스 내부 self에 담기게 된다.
# self.first 는 a.first 와 같은 말이고, 전달된 객체 내부에 first 라는 변수를 만들기 때문에 "객체 변수" 혹은 "속성" 이라고 부른다.

a = FourCal() # 여기서 FourCal() 은 클래스의 인스턴스를 만들고, 만든 인스턴스를 a 에 담고 있다. 
# a.setdata(3, 4) # 함수는 위치 인수로 값을 전달 해야 하는데 구현부를 보면 매개변수로 3개의 변수를 정의하고 있다. 하지만 전달 되는 값은 2개 이다.
# 클래스 내부에 self 는 위에서 말했든 특별한 매개 변수로 자동으로 a객체 자신을 전달한다. FourCal.setdata(a, 3, 4) 이렇게 전달하는것과 같다.

# print(a.add()); # error 발생

# a.setdata(3, 4)

# print(a.add());
# print(a.mul());
# print(a.sub());
# print(a.div());

# __init__ -> 인스턴스가 생성이 될때 자동으로 실행이 되는 메소드 무조건 실행이 된다.
# __init__ 이 없다면 구현한 계산기 앱에서 setdata() 메소드를 호출 해주지 않으면 오류가 발생한다. 내부에


class FourCal1:
  def __init__(self, first, second):
    self.first = first
    self.second = second
  def setdata1(self, first, second): # self(필수) -> 자기 자신을 의미 [클래스를 생성한 인스턴스를 담은 객채가 setdata함수가 실행이 될때 self에 담기게 된다]
    self.first = first
    self.second = second
  def add1(self):
    result = self.first + self.second
    return result
  def mul1(self):
    result = self.first * self.second
    return result
  def sub1(self):
    result = self.first - self.second
    return result
  def div1(self):
    result = self.first / self.second
    return result

b = FourCal1(3, 4) # 인스턴스를 생성하는 순간 __init__ 실행되어 first, second 값을 넘겨 주어야 인스턴스가 생성이 되고, b 에 담기게 된다.
print(b.add1());



# class 상속
# 상속 받은 클래스의 기능을 사용할 수 있지만, __init__ 메소드는 새롭게 정의 해줘야 동작을 한다. 초기화 과정이 필요하다면.
# 클래스 내부에 메소드는 반드시 self 매개변수를 받아야 한다.
class MoreFourCal(FourCal1):
  def __init__(self, first, second): # 자식 클래스에서 새롭게 생성자 메소드도 자식요소에서 새롭게 정의하면 오버라이딩 된다.
    # 여기서 문제는 부모의 생성자 메소드가 실행되지 않아 자식 인스턴스 객체에서 부모의 메소드를 사용하려 하면 에러 발생한다. 
    # 문제 해결은 super().__init__(first, second) 사용하여 해결한다.
    self.first = first
    self.second = second
  def pow(self):
    result = self.first ** self.second
    return result
  def strPrint(self):
    print('more four cal 인스턴스 입니다.')
  

v = MoreFourCal(2, 4);
# print(f"more-four-cal add() :", v.add()); # 부모의 생성사 메소드가 실행되지 않아 초기 값이 없는 상태여서 에러 발생.
print(f"more-four-cal pow() :", v.pow());
v.strPrint()


# 메소드 오버라이딩
class SafeFourCal(FourCal1):
  def __init__(self, safeFirst, safeSecond):
    super().__init__(safeFirst, safeSecond) # __init__ 은 인스턴스가 생성되는 시점에 실행이 되지만 상속을 받아 자식 클래스 인스턴스가 실행이 될때
    # 부모 클래스의 인스턴스는 실행이 되지 않고, 그렇기 때문에 부모 클래스에 정의된 __init__ 메소드가 호출 되지 않는다. 따라서
    # super() 함수를 실행하므로 임시적으로 부모 클래스의 객체를 가지고 오고 .__init__으로 생성자 함수를 실행하여 클래스의 초기화를 진행한다.
    # 즉 a = FourCal(2, 3) 와 super().__init__(sefeFirst, safeSecond) 는 동일한 개념이라고 보면 된다.
  def div(self): # 부모와 같은 이름의 메소드를 작성하면 부모의 메소드가 실행되지 않고, 자식 클래스의 메소드가 실행이 된다. 이걸 메소드 오버라이딩이라 한다.
    if self.second == 0:
      return 0;
    else:
      result = self.first / self.second
      return result


d = SafeFourCal(2, 0);
print(d.div());