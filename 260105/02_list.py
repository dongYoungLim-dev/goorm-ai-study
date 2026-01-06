# 리스트형
list1 = [1, 2, 3, 4, 5]
list2 = [10, 20, 30, 40]
list3 = [1, 2, 3, 2, 2, 4]
list4 = [3, 1, 4, 2]
list5 = [1, 2, 3]

# 1.리스트 [1, 2, 3, 4, 5]의 모든 요소의 합을 출력하라.
sumList = sum(list1);
print(sumList); # 15 출력

# 2.리스트 [1, 2, 3, 4, 5]에서 짝수만 담은 새 리스트를 만들어 출력하라.
evenNum1 = list(filter(lambda x : x % 2 == 0, list1));
evenNum2 = [x for x in list1 if x % 2 == 0]
evenNum3 = []
for x in list1:
  if x % 2 == 0:
    evenNum3.append(x);

print(evenNum1); # [2, 4] 출력
print(evenNum2); # [2, 4] 출력
print(evenNum3); # [2, 4] 출력


# 3.리스트 [3, 1, 4, 2]를 오름차순으로 정렬하여 출력하라.
sortList = list4;
sortList.sort()
print(sortList); # [1, 2, 3, 4] 출력

# 4.리스트 [10, 20, 30, 40]에서 최댓값을 출력하라.
print(max(list2)) # 40 출력
maxNum = 0
maxList = [1, 5, 4, 6, 7, 9]
for i in range(len(maxList)):
  if maxNum < maxList[i]:
    maxNum = maxList[i]

print(maxNum); # 9 출력


# 5.리스트 [10, 20, 30, 40]에서 최솟값을 출력하라.
print(min(list2)) # 10 출력
minList = [4, 2, 5, 7, 8, 3]
minNum = minList[0];
for i in range(len(minList)):
  if minNum > minList[i]:
    minNum = minList[i];
print(minNum); # 2 출력

# 6.리스트 [1, 2, 3, 4, 5]를 역순 리스트로 만들어 출력하라.
reverseList = list1;
reverseList.reverse();
print(reverseList); # [5, 4, 3, 2, 1] 출력

# 7.리스트 [1, 2, 3, 2, 2, 4]에서 숫자 2가 몇 번 등장하는지 출력하라.
print(list3.count(2)); # 3 출력

# 8.리스트 [1, 2, 3]에 숫자 4를 추가한 뒤 출력하라.
appendList = list5;
appendList.append(4);
print(appendList); # [1, 2, 3, 4] 출력

# 9.리스트 [1, 2, 3, 4, 5]에서 인덱스 1 ~ 3까지 슬라이싱하여 출력하라.
list1.reverse();
print(list1[1:3]); # [2, 3] 출력
print(list1[:3]); # [1, 2, 3] 출력

# 10.리스트 안의 숫자들을 모두 문자열로 바꾼 리스트를 만들어 출력하라.
numToStr = list(map(str, list2));
print(numToStr); # ['10', '20', '30', '40'] 출력

numToStr2 = []
for i in range(len(list2)):
  numToStr2.append(str(list2[i]));
print(numToStr2); # ['10', '20', '30', '40'] 출력