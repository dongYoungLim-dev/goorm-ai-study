# 집합 자료형
# 문제 1. (기초 생성) 비어 있는 집합 my_set을 생성하는 코드를 작성하세요. (주의: {}는 사용하면 안 됩니다.)
s1 = set();
print(type(s1)); # <class 'set'> 출력

# 문제 2. (중복 제거) 리스트 nums = [1, 2, 2, 3, 3, 3, 4]가 있습니다. 이 리스트에서 중복을 모두 제거하고 유일한 숫자들만 남긴 집합 unique_nums를 만드세요.
nums = [1, 2, 2, 3, 3, 3, 4]
nuique_nums = set(nums);  # set 은 중복을 허용하지 않고, 순서가 없는 자료형이다. 중복이 허용된 리스트를 인자로 넘기면 자동으로 중복을 제거 한다.
print(nuique_nums); # {1, 2, 3, 4} 출력

# 문제 3. (값 추가) 집합 s = {1, 2, 3}이 있습니다. 여기에 숫자 4를 추가하는 코드를 작성하세요.
s = {1, 2, 3}
s.add(4);
print(s); # {1, 2, 3, 4} 출력

# 문제 4. (여러 값 추가) 집합 s = {1, 2}가 있습니다. 여기에 리스트 [3, 4, 5]에 들어있는 값들을 한꺼번에 추가하는 코드를 작성하세요.
s2 = {1, 2}
s2.update([3, 4, 5])
print(s2); # {1, 2, 3, 4, 5} 출력

# 문제 5. (안전한 삭제) 집합 s = {1, 2, 3}에서 값 5를 삭제하려고 합니다. 만약 5가 없더라도 에러가 나지 않도록 삭제하는 메서드를 사용하세요.
s3 = {1, 2, 3}
s3.discard(4); # discard는 없는 값을 삭제 하더라고 오류 발생 X
print(s3); # {1, 2, 3} 출력

# 문제 6. (교집합) 두 집합 A = {1, 2, 3, 4}와 B = {3, 4, 5, 6}이 있습니다. 두 집합에 모두 포함된 요소만 뽑아서 출력하세요.
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
print(A & B); # {3, 4} 출력 
print(A.intersection(B)); # {3, 4} 출력
# & , intersection() 두개모두 동일한 동작을 한다.

# 문제 7. (합집합) 위의 두 집합 A와 B의 모든 요소를 합치되, 중복은 제거하여 출력하세요.
print(A | B); # {1, 2, 3, 4, 5, 6} 출력
print(A.union(B)); # {1, 2, 3, 4, 5, 6} 출력
# | , union() 두개 모두 동일한 동작을 한다.

# 문제 8. (차집합) 집합 A에는 있는데 B에는 없는 요소(1, 2)만 남기는 코드를 작성하세요.
print(A - B); # {1, 2} 출력
print(A.difference(B)); # {1, 2} 출력
print(B - A); # {5, 6} 출력
print(B.difference(A)); # {5, 6} 출력

# 문제 9. (문자열 처리) 문자열 "Hello World"에 들어있는 '알파벳 종류'가 총 몇 개인지 구하는 코드를 작성하세요. (공백 포함 여부는 상관없음, 대소문자는 구분함)
str = "Hello World"
noSpace = str.replace(" ", "");
setVal = set(noSpace);
print(setVal);

lowerNum = 0;
upperNum = 0;
for val in setVal:
  if val.islower():
    lowerNum += 1;
  else:
    upperNum += 1;
print(f"Hello World 에 중복을 제거하고 대문자 {upperNum}개, 소문자 {lowerNum}개 있다.");

# 문제 10. (부분집합 확인)sub = {1, 2}이고 main = {1, 2, 3, 4}입니다. sub가 main의 부분집합이 맞는지 확인하여 True가 출력되게 하세요.
sub = {1, 2}
main = {1, 2, 3, 4}

if sub < main:
  print(True);
else:
  print(False);