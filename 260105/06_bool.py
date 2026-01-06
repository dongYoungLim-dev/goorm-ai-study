# 불(Bool) 자료형
# 문제 1. (기초 비교) 숫자 10이 5보다 큰지 비교하여 그 결과(True)를 출력하세요.
if 10 > 5:
  print(True);
else:
  print(False);

# 문제 2. (동등 비교) 숫자 1과 문자열 "1"이 같은지 비교하는 코드를 작성하세요. (결과는 False여야 합니다.)
if "1" == 1:
  print(True);
else:
  print(False);

# 문제 3. (논리 연산 AND) 변수 a = 10입니다. a가 5보다 크고(and) 20보다 작은지 확인하는 코드를 작성하세요.
a = 10 
if a > 5 and a < 20:
  print(True);
else:
  print(False);

# 문제 4. (논리 연산 OR) 변수 color = "Red"입니다. color가 "Red" 이거나(or) "Blue"인지 확인하는 코드를 작성하세요.
color = "Blue" # Red = True, Blue = True, Black = False

if color == "Red" or  color == "Blue":
  print(True);
else:
  print(False);

# 문제 5. (논리 부정 NOT) 변수 is_open = False입니다. 이 값의 반대인 True를 출력하는 코드를 작성하세요.
is_open = False # False = True 출력,  True = False 출력
if not is_open:
  print(True);
else:
  print(False);

# 문제 6. (자료형의 참/거짓 1) 빈 리스트 []를 bool() 함수에 넣었을 때 어떤 값(True/False)이 나오는지 출력하세요.
listVal = [] # [] => False, [1,2] => True
print(bool(listVal)); # False

# 문제 7. (자료형의 참/거짓 2) 숫자 0이 아닌 -5를 bool() 함수에 넣었을 때의 결과를 출력하세요.
print(bool(-5)); # True 출력 -5는 음수 값이 지만 0이 아니기 때문에 True 출력

# 문제 8. (범위 확인 간소화) 변수 score = 85입니다. 이 점수가 80점 초과이고 90점 미만인지 파이썬 특유의 연속된 부등호(a < x < b)를 사용하여 확인하세요.
score = 85
print(80 < score < 90) # True 출력

# 문제 9. (짝수 판별) 변수 n = 4입니다. n을 2로 나눈 나머지가 0인지 확인하여 짝수라면 True가 나오게 하세요.
n = 4

if n % 2 == 0:
  print(True);
else:
  print(False);

# 문제 10. (None 확인) 변수 val = None입니다. 이 변수가 None이라는 것을 확인하는 가장 올바른 조건식(is 사용)을 작성하세요.
val = "None" # "None" => False, None => True

if val is None:
  print(True);
else:
  print(False);