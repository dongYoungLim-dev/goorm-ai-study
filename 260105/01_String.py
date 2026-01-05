# 문자형
s = "String length count"
c = "Any good ideas python"

# 1.문자열 s가 주어질 때 문자열의 길이를 출력하라.
print(len(s)); # 19 출력

# 2.문자열 s가 주어질 때 첫 글자와 마지막 글자를 출력하라.
print(s[0]); # S 출력
print(s[len(s) - 1]) # t 출력
print(s[-1]) # t 출력

# 3.문자열 s가 주어질 때 문자열을 모두 대문자로 변환하여 출력하라.
upper = s.upper();
print(upper); # STRING LENGTH COUNT 출력

# 4.문자열 s가 주어질 때 문자열을 모두 소문자로 변환하여 출력하라.
lower = s.lower();
print(lower); # string length count 출력

# 5.문자열 s가 주어질 때 문자열에 'a'가 몇 개 있는지 출력하라.
print(s.count('a')); # 0 출력
print(c.count('a')); # 1 출력

# 6.문자열 s가 주어질 때 문자열을 거꾸로 출력하라.
# 슬라이싱의 [시작:끝:규칙] 1 = 정방향으로 한칸씩, 2 = 앞에서 부터 두칸씩, -1 = 역방향으로 한칸씩, -2 = 뒤에서 두칸씩 잘라서 보여 준다.
print(s[::-1]); # tnuoc htgnel gnirtS 출력

# 7.문자열 s가 주어질 때 'python'이라는 단어가 포함되어 있으면 True, 아니면 False를 출력하라.
print("python" in s); # False 출력
print("python" in c); # True 출력


# 8.문자열 "hello world"에서 공백을 제거한 문자열을 출력하라.
l = "hello world"
print(l.replace(" ", "")); # helloworld 출력

# 9.문자열 s가 주어질 때 문자열이 회문인지 True / False로 출력하라.
# 방법 1 True 출력
w = "radar";
w_reverse = w[::-1];

if w == w_reverse:
  print("true");
else:
  print("false");

#방법 2 True 출력
for i in range(len(w) // 2): # 문자열 길이의 절반 만큼 반복
  if w[i] != w[-1 - i]: 
    print('false');
    break
  print('true');


# 10.문자열 "abc123"에서 숫자만 추출해서 출력하라.
g = "abc123"
print(g[3:]); # 슬라이스 방법