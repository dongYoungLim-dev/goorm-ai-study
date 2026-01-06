# 튜플형
s = (1, 2, 3, 4)
# 1.튜플 (1, 2, 3, 4)의 길이를 출력하라.
print(len(s)); # 4 출력

# 2.튜플 (10, 20, 30)에서 첫 번째 값을 출력하라.
d = (10, 20, 30)
a, b, c = (10, 20, 30)
print(a) # 10 출력
print(d[0]) # 10 출력

# 3.튜플 (10, 20, 30)을 리스트로 변환하여 출력하라.
l = (1, 2, 3)
tupleToList = list(l);
print(tupleToList); # [1, 2, 3] 출력

# 4.튜플 (1, 2, 3)에 (4, 5)를 붙여 새 튜플을 만들어 출력하라.
v = (1, 2, 3)
x = (4, 5)
result = v + x;
print(result); 

# 5.튜플 (1, 2, 3, 2, 2)에서 숫자 2의 개수를 출력하라.
tuple2 = (1, 2, 3, 2, 2)
print(tuple2.count(2)); # 3 출력

# 6.튜플 (10, 20, 30)을 a, b, c로 언패킹하여 출력하라.
a, b, c = (10, 20, 30)
print(a);
print(b);
print(c);

# 7.튜플 (5, 1, 3)을 정렬된 리스트로 변환하여 출력하라.
tuple3 = (5, 1, 3)
tupleSort = list(tuple3);
tupleSort.sort()
print(tupleSort); # [1, 3, 5] 출력

# 8.튜플 안에 숫자 4가 있는지 True / False로 출력하라.
tuple4 = (1, 2, 3, 4, 5) # Ture 출력
tuple5 = (1, 2, 3, 5) # False 출력
if 4 in tuple4:
  print(True)
else:
  print(False)

# 9.리스트 [1, 2, 3]을 튜플로 변환하여 출력하라.
exList = [1, 2, 3]
listToTuple = tuple(exList);
print(listToTuple); # (1, 2, 3) 출력

# 10.튜플이 수정 불가능한 자료형임을 코드로 확인해보라 (에러 발생 확인)
listToTuple[0] = 3; # TypeError: 'tuple' object does not support item assignment