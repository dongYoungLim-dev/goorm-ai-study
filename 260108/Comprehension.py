# Comprehension 문법

# 한줄에 연산작용, 반복문, 조건문을 담아서 처리가 가능한 문법

test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# even = [for i in test] # 첫 단계 for in 을 이용하여 반복문을 작성한다. 이렇게만 작성하면 error
# even = [i for i in test] # 리스트에 담길 요소를 for 앞에 작성한다. 반복문에서 요소가 담길 변수와 같게 써줘야 한다.
# even = [i for i in test if i % 2 == 0] 반복문이 끝나는 지점에 한칸 띄우고 조건문을 적으면 
# 반복문으로 iterable 자료형을 순회 하면서 i 담아 조건문을 통과 시키고, 이때 True인 요소만 리스트에 담길 요소 즉 첫 번째 i에 담기게 된다.

even = [i for i in test if i % 2 == 0] 
print(even) # [2, 4, 6, 8, 10] 출력 -> test list를 순회 하면서 조건문을 통과 했을때 짝수만 i 에 담기고 최종적으로 짝수만 담은 even이 만들어 진다.

even2 = [i+1 for i in test if i % 2 == 0]
print(even2) # [3, 5, 7, 9, 11] 출력, 마지막에 담을 때 연산작용까지 가능하다.

even3 = [i**2 for i in test if i % 2 == 0]
print(even3) # [4, 16, 36, 64, 100] 출력, 제곱 

# 겉을 감싸는 괄호의 모양에 따라 list, set, dictionary 형태로 반환된다.
# dictionary 형태의 주의사항 반드시 key:value 형태로 담아야 한다.

even4 = {i:i**2 for i in test if i % 2 == 0}
print(even4) # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100} 출력

dictVal = {'a':1, 'b':2, 'c':3}
even5 = {key:i+1 for key, i in dictVal.items() if i > 0} # 직접 dictionary 만들어 전달하는 경우 .items()를 이용하여 key:value 한쌍식 전달을 해야 한다.
print(even5);


# zip 활용
sample_data4 = [1, 2, 3, 4]
sample_data5 = ['홍길동', '김철수', 'home', 'join']
tupleVal = {key:i for key, i in zip(sample_data4, sample_data5)} # tuple 의 언패킹을 이용하여 key, i 값을 받고 이를 dictionary key:value 형태로 변경한다. zip() 함수를 이용하여.
print(tupleVal) # {1: '홍길동', 2: '김철수', 3: 'home', 4: 'join'} 출력