def sumMultiple():
  n = 1
  while n < 1000:
    if n % 3 == 0 or n % 5 == 0:
      n += n
    n += 1;
  
  print(f"1 부터 1000 미만의 자연수 중 3과 5의 배수의 합 : {n}");



def commonMultiple():
  n = 1
  while n < 1000:
    if n % 3 == 0 and n % 5 == 0:
      print(f"3과 5의 모두 속한 자연수 : {n}")
    n += 1;


print('='*20)
sumMultiple();
print('3과 5의 공배수')
commonMultiple();