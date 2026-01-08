# Filter 값을 필터링을 할때 사용한다. 필터링 기준은 True 값을 가지는 요소만 필터링 된다.
# Map 과 동일하게 함수와 iterable한 자료형을 인수로 전달한다.
sample_data = [1, 2, 3, 4, 5, 6, 7, 8, 9]

result = filter(lambda x : True if (x % 2 == 1) else False, sample_data) # 정의된 함수에서 조건문을 통과 했을때 True인 값만 필터링 된다.
print(list(result)) # [1, 3, 5, 7, 9] 출력

# 직접 정의한 함수 전달
def three_multiple(x):
  if x % 3 == 0:
    return True
  else:
    return False
result1 = filter(three_multiple, sample_data)
print(list(result1)); # [3, 6, 9] 출력

