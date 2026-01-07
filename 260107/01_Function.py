# 함수의 3가지 형태

# 01. 입력 매개변수 O, return O
def sample_function(a, b):
  result = a + b
  return result

# 02. 입력 매개변수 O, return X
def sample_function2(a, b):
  result = a + b
  print(f'result: {result}')

# 03. 입력 매개변수 X, return x
def sample_function3():
  print('Hello World')


sample_function # 이름만 작성
sample_function3() # 함수 콜(Call)
a = sample_function3 # 함수 자체를 변수에 담는다.
a()

b = sample_function3() # return 값이 없기 때문에 함수는 None을 반환하고 이를 변수에 담는다.
print(b);

c = sample_function(1, 2); # 함수 내부 return 으로 반환된 값을 변수에 담는다.
print(c);

def string_doc():
  """
  Docstring for string_doc
  이 함수를 사용하는 대상에게 함수에 대한 설명 
  및 호출 예시를 작성한다.
  반드시 함수 선언부 바로 다은줄에 작성한다.
  """
  print("Hello World")

print(string_doc.__doc__); # 함수 내부에 작성된 doc 내용을 확인하는 방법
print(print.__doc__) # doc을 확인하고 싶은 키워드 뒤에 .__doc__ 을 사용하여 확인 가능하다.



# 인수, 매개변수

def add_fun(a, b): # 함수 선언시 함수가 받을 값의 변수 -> 매개변수(parameter)
  result = a + b
  print(result)

add_fun(1, 3) # 함수 실행시 함수로 전달하는 값 -> 인수(argument)

# 위치 인수
def add_fun1(a, b, c): # 함수 실행시 전달한 인수가 각각 a = 1, b = 2, c = 3 할당된다.
  result = a + b + c
  print(result);
add_fun1(1, 2, 3) # 위치 인수는 반드시 순서를 준수해야 하며, 함수 선언부에 전달 받을 매개변수와 전달 하는 인수의 수가 같아야 한다. 적거나 많은 경우 에러 발생

# 키워드 인수
def add_fun2(a, b, c): # 매개변수로 선언한 값에 직업 인수 전달 a = 1, b = 2, c = 3 으로 할당 된다.
  result = a + b + c
  print(result);
add_fun2(a=1, b=2, c=3); # 키워드 인수는 함수 선언부에 선언한 매개 변수 명을 지정하여 인수 전달, 매개변수 명과 일치만 하면 전달 순서는 상관 없다.

# 기본 매개변수
# (기본 매개변수는 위치 인수 값을 받는 매개 변수 뒤에 있어야 한다. 그렇지 않으면 에러 발생 [add_fun3(a=1, b, c) => 에러 발생])
def add_fun3(a, b=1, c=2): # 매개변수의 default 값을 설정하여 함수 실행부에서 인수를 매개변수 수와 다르게 전달 하여도 기본값으로 실행이 된다.
  result = a + b + c
  print(result);
add_fun3(1) # 매개변수에 기본값이 설정되어있으면 해당 인수는 전달 하지 않아도 함수는 실행이 된다.
add_fun3(1, 2, 3) # 기본값이 설정되어있어도 값을 전달하면 전달된 값으로 덮어쓰기 된다.


# 가변 매개변수(tuple)
def add_func(*args): # 가변 인자 => 몇개가 인수로 전달 될지 모르는 상황에서 사용 몇개가 들어오든 받아서 튜플 형태로 매개 변수에 담긴다.
  result = int();
  for a in args:
    result += a
  print(f"result: {result}")

add_func(1, 2, 4, 5) # 4개 전달
add_func() # 0개 전달
add_func(1, 2) # 2개 전달
tupleVal = (1, 2, 3)
add_func(*tupleVal) # tuple 을 직접 만들어서 전달도 가능하지만 전달 할때는 변수명 앞에 * 을 붙여주어야 한다. (*을 붙이게 되면 언패킹된다.)
# 가변 매개변수는 전달 하지 않아도 혹은 몇개를 전달하든 함수가 실행된다.

# 위치 인수 + 가변 매개변수 사용시 반드시 가변 매개 변수는 위치 인수 뒤에 와야 한다.
def add_func01(a, *args):
  result = int();
  for a in args:
    result += a
  print(f"위치 인수 : {a} result: {result}")

add_func01(1) # 위치 인수는 반드시 값을 넘겨 줘야 하기 때문에 아무것도 넘기지 않으면 에러 발생 위치 인수만 할당 해주면 실행 가능

# 가변 매개변수(dict) 관례로 **kwargs 로 입력한다.
def add_func01(**kwargs): # dictionary 형태로 전달된 인수를 변환하여 담긴다.
  for key, value in kwargs.items():
    print(f"key:{key} value: {value}")

add_func01(apple=1, test=2, home=3) # dictionary 가변 매개변수로 설정되면 인수가 반드시 key=value 형태로 전달이 되어야 한다.
dictVal = {'apple': 1, 'test': 2, 'home': 3}
add_func01(**dictVal) # 직접 dictionary 를 만들어 전달하는 경우 변수명 앞에 **을 붙여 주어야 한다. 이때 언패킹 처리가 된다.




# 익명함수(lambda) 이름없이 작성된 함수
lambdaFun = lambda x : x * 2 # lambda 함수는 : 기준으로 왼쪽 (lambda x) 가 매개 변수가 된다. : 기준으로 오른쪽 (x * 2) 함수 실행부 이다.
# return 구문은 없지만 결과 값을 반환하게 되어있다.
v = lambdaFun(4)
print(v)

# lambda 함수도 위치 인자, 기본 값이 적용된 매개 변수를 사용 할 수 있다.
lambdaFun2 = lambda x, y: x + y
v2 = lambdaFun2(1, 2)
print(v2);

lambdaFun3 = lambda x, y=10: x * y
v3 = lambdaFun3(1);

# 삼항 연산을 사용함 lambda
lambdaFun4 = lambda x: x + 1 if x > 2 else x
v4 = lambdaFun4(1) # 1 출력
v5 = lambdaFun4(3) # 4 출력
print(f"v4 : {v4}");
print(f"v5 : {v5}");
