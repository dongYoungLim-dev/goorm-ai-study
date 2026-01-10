def gugudan(dan):
  '''
  Docstring for gugudan
  
  :param dan: 구구단을 단을 int 값으로 입력해주면 해당 "단"을 계산하여 출력
  '''
  i = 1
  print(f"{dan}단")

  while i < 10:
    print(f"{dan} * {i} = {dan * i}");
    i += 1;

gugudan(2);
print('='*20)
gugudan(3);
