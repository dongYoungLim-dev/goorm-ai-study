# 딕셔너리
dictVal = {"a": 1, "b": 2}
# 1.딕셔너리 {"a": 1, "b": 2}에서 key "a"의 값을 출력하라.
print(dictVal.get("a")) # 1

# 2.딕셔너리 {"a": 1}에 "b": 2를 추가하여 출력하라.
dictVal2 = {"a": 1}
dictVal2["b"] = 2
dictVal2["c"] = 3
print(dictVal2.get("b"))
print(dictVal2) # {"a": 1, "b": 2, "c": 3} 출력

# 3.딕셔너리 {"a": 1, "b": 2}에서 모든 key를 출력하라.
dictVal3 = {"a":1 , "b": 2, "c": 3}
dictKeys = dictVal3.keys();
print(dictKeys); # dict_keys(['a', 'b', 'c']) 출력

# 4.딕셔너리 {"a": 1, "b": 2}에서 모든 value를 출력하라.
dictValues = dictVal3.values();
print(dictValues); # dict_values([1, 2, 3]) 출력

# 5.딕셔너리 {"a": 1, "b": 2}에서 key "c"가 없으면 0을 출력하라.
if 'd' in dictVal3: 
  print(dictVal3['d']);
else:
  print(0);
# 0 출력

# 6.딕셔너리 {"apple": 3, "banana": 5}에서 "apple"의 값을 10으로 변경하라.
dictVal4 = {'apple': 3, 'banana': 5}
dictVal4['apple'] = 10;
print(dictVal4); # {'apple': 10, 'banana': 5} 출력

# 7.딕셔너리 {"a": 1, "b": 2}에서 key "b"를 삭제하라.
dictVal5 = {'a': 1, 'b': 2}
del dictVal5['b']
print(dictVal5); # {'a': 1} 출력

# 8.딕셔너리의 모든 key와 value를 한 줄씩 출력하라.
for key, value in dictVal4.items():
  print(f"key: {key}, value: {value}");
# key: apple, value: 10 출력
# key: banana, value: 5 출력

# 9.리스트 [("a", 1), ("b", 2)]를 딕셔너리로 변환하여 출력하라.
listVal = [('a', 1), ('b', 2)];
dictVal6 = {}
for item in listVal:
  key, value = item
  dictVal6[key] = value

print(dictVal6); # {'a': 1, 'b': 2} 출력

# 10.딕셔너리 {"a": 1, "b": 2, "c": 3}에서 value의 합을 출력하라.
dictVal7 = {'a': 1, 'b': 2, 'c': 3}
sumNum = 0
for value in dictVal7.values():
  sumNum = sumNum + value
print(sumNum) # 6 출력