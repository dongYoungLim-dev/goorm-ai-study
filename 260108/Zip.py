# Zip iterable 한 자료형을 받지만 가변인자로 받게 된다.
# zip(*iterable)

sample_data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
sample_data2 = [11, 12, 13, 14, 15, 16, 17, 18, 19]
sample_data3 = [99, 98, 97]

# zip 은 전달 받은 인자의 같은 인덱스의 값을 tuple 형태로 묶어준다. 
# 전달된 인수의 값의 수가 다른 경운 스마트 하게 작은 수의 데이터에 맞추어서 데이터를 반환하고 종료 된다.
print(list(zip(sample_data1, sample_data2))); # [(1, 11), (2, 12), (3, 13), (4, 14), (5, 15), (6, 16), (7, 17), (8, 18), (9, 19)] 출력
print(list(zip(sample_data1, sample_data2, sample_data3))) # [(1, 11, 99), (2, 12, 98), (3, 13, 97)] 출력 sample_data3 데이터가 3개 여서 3개만 출력.

# zip 활용
sample_data4 = [1, 2, 3, 4]
sample_data5 = ['홍길동', '김철수', 'home', 'join']
dictVal = {}

for number, name in zip(sample_data4, sample_data5): # zip 이 tuple 형태로 데이터를 묶기 때문에 tuple의 언패킹이 가능하다. 
  dictVal[number] = name # 언팩된 tuple 요소를 가지고 딕셔너리 형태로 변환도 가능하다.

print(dictVal); # {1: '홍길동', 2: '김철수', 3: 'home', 4: 'join'} 출력
