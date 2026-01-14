# iterator 
# 데이터를 하나씩 꺼내 올 수 있는 객체.

a = [1, 2, 3]
# next(a)
# a 리스트를 이용하여 next를 호출 했더니, 이터에이터 객체가 아니라는 오류 발생 TypeError: 'list' object is not an iterator
# 즉 반복 가능한 타입이 모두 이터레이터는 아니게 된다.
# 반복이 가능하다면 iter 함수를 이용하여 이터레이터를 만들 수 있다.


ia = iter(a);
print(type(ia)); # <class 'list_iterator'>

print(f"1. {next(ia)}"); # 1. 1
print(f"2. {next(ia)}"); # 2. 2
print(f"3. {next(ia)}"); # 3. 3
# print(next(ia)) # StopIteration 예외 발생 후 종료



# 직접 iterarot 클래스 구현

class MyIterator:
  def __init__(self, data):
    self.data = data
    self.position = 0
  
  def __iter__(self): # 해당 메소드가 있어야 파이썬은 반복 가능한 객체로 인식한다.
    return self
  
  def __next__(self):
    if self.position >= len(self.data): # position 이 data의 길이보다 크면
      raise StopIteration               # StopIteration 예외를 내보내고.
    result = self.data[self.position]   # position 값에 해당하는 인덱스의 값을 result 에 담고,
    self.position += 1                  # position 값을 하나 증가 시켜 준다.
    return result                       # position 위치의 값을 반환한다.
  

if __name__ == '__main__':
  i = MyIterator([1, 2, 3])
  for item in i:
    print(item)  



# generator
# generator 는 함수와 모양은 같지만 반환 키워드가 return, yield 처럼 다르다.
def mygen():
  yield 'a'
  yield 'b'
  yield 'c'


g = mygen() # 여기서 g 에는 generator 객체 상자가 담기게 되고,

print(next(g)) # a next 에 g를 전달하여 실행 시키면 상자 안에 첫번째 값이 반환되고, g의 generator 객체는 일시정지 상태가 된다.
print(next(g)) # b next 에 g를 전달하여 실행 시키면 상자 안에 두번째 값이 반환되고, g의 generator 객체는 일시정지 상태가 된다.
print(next(g)) # c next 에 g를 전달하여 실행 시키면 상자 안에 번째 값이 반환되고, g의 generator 마지막 값이므로 StopIteration 예외를 발생하며 종료 된다.