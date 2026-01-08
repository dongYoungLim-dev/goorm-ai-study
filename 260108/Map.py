# 내장함수 (built-in function)
# 이미 구현 되어 내장된 함수

#Map
# 함수와 순회 가능한 iterable한 자료형을 입력값으로 받아 iterable한 자료형의 각 요소를 하나하나 함수로 전달하여 처리를 하고 수행 결과를 묶어서 전달 하는 내장함수 이다.

sample_data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = list(map(str, sample_data)) # 파이썬에 정의된 내장함수도 전달 할수 있다. str 함수는 전달된 값을 문자열로 변환한다.
print(result); # ['1', '2', '3', '4', '5', '6', '7', '8', '9'] 출력

# map 함수는 다중 인수도 지원 한다.
sample_data1 = [1, 2, 3]
sample_data2 = [4, 5, 6]
result2 = list(map(lambda x, y: x + y, sample_data1, sample_data2)) # map 함수에 lambda 함수도 전달이 가능하다. 
print(result2); # [5, 7, 9] 출력
# 데이터 수, 차이가 나면?
sample_data3 = [1, 2, 3, 4, 5]
sample_data4 = [6, 7, 8]
result3 = list(map(lambda x, y: x + y, sample_data3, sample_data4)) # 전달되는 인수의 데이터의 수가 다르면 작은 수의 데이터에 자동으로 맞추어 결과를 반환한다.
print(result3); # [7, 9, 11] 출력


