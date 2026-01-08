# Enumerate
# iterable 자료형을 전달 받고, start index 를 두번째 매개변수로 받는다.
# (start:end(미만):stap)
for i in range(1, 10, 2):
  print(f"default value = {i}");  # 1 - 9 까지 출력 됨

#enumerate 는 index + value 를 쌍으로 반환한다.
for i in enumerate(range(1, 10, 2), start=100): # start를 100으로 지정하면 index가 100부터 시작한다.
  index, value = i
  print(f"range_index:{index}, range_value: {value}")


sample_data = [1, 2, 3, 4, 5, 6, 7]
sample_data4 = [11, 12, 13, 14, 15, 16, 17]
sample_data5 = [99, 98, 97, 96, 95, 94, 93]
sample_data2 = (1, 2, 3, 4, 5, 6)
sample_data3 = {'a': 1, 'b': 2, 'c': 3, 'd': 5}

for i in enumerate(sample_data, start=0):
  index, value = i
  print(f"list_index: {index}, list_value: {value}");

for i in enumerate(sample_data2, start=0):
  index, value = i
  print(f"tuple_index: {index}, tuple_value: {value}");

for i in enumerate(sample_data3, start=0): # dictionary 자료형은 key : value 형태이기 때문에 i = index, key가 담긴다. key가 아니라 value 를 담고 싶으면 .values() 함수를 이용하여 dictionary 의 value값을 반환 해야 한다.
  index, key = i
  print(f"dict_index: {index}, dict_value: {value}");