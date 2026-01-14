import time

#decorator

def elapesd(func):
  def wrapper():
    start = time.time()
    result = func()
    end = time.time()
    print(f"함수 실행시간: {end - start}")
    return result
  return wrapper

@elapesd # @ + 실행시킬 함수명 을 입력하여 a = elapesd(myFunc) // a() 와 동일하다.
def myFunc():
  print("함수가 실행됩니다.")

myFunc()

# decorator은 함수의 인수로 함수를 전달하여 새로운 기능을 함수를 변경하지 않고, 추가 하고 싶은 경우 사용
# elapesd 함수로 myFunc를 전달하여 elapesd = 함수1 내부에 또다른 wrapper = 함수2에 담고.  함수2를 함수1의 실행 결과로 반환하는 과정에서 
# 클로저의 개념이 나온다. wrapper함수 내부에 전달된 함수를 담아 외부에서 전달된 함수의 기본 기능 + wrapper 함수에 정의된 기능까지 추가로 동작된다.
# 이를 decorator라고 부른다.


# __call__ 메소스

class Mul:
  def __init__(self, m):
    self.m = m


  def mul(self, n): 
    return self.m * n
  
if __name__ == "__main__":
  mul3 = Mul(3)
  mul5 = Mul(5)

  print(mul3.mul(10))
  print(mul5.mul(20))


# 위 함수를 아래처럼 변경 가능하다.

class Mul1:
  def __init__(self, m):
    self.m = m

  def __call__(self, n): # __call__ 클래스 호출문을 만나면 그 즉시 실행이 되는 메소드이다.
    return self.m * n
  
if __name__ == "__main__":
  mul4 = Mul1(4)
  mul6 = Mul1(6)

  print(mul4(10))
  print(mul6(20))
