import numpy as np
import pandas as pd



'''
개요
sort_values 메서드는 값을 기준으로 레이블을 정렬하는 메서드입니다.

사용법

기본 사용법
df.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)
by : 정렬 기준이될 레이블입니다.
axis : {0 : index / 1: columns} 정렬할 레이블입니다. 0이면 행, 1이면 열을 기준으로 정렬합니다.
inplace : 원본을 대체할지 여부입니다. True일 경우 원본을 대체하게 됩니다.
kind : 알고리즘 모드 입니다. 모드는 총 4종으로 quicksort, mergesort, heapsort, stable이 있는데,
속도와 효율성의 차이를 갖습니다. 기본적으로 quicksort이며, 자세한건 numpy doc에서 확인 가능합니다.
na_position : {first / last} Na값의 위치입니다. 기본값은 last로 정렬시 맨 뒤에 위치합니다.
ignore_index : 인덱스의 무시 여부입니다. True일 경우 인덱스의 순서와 상관없이 0,1,2,... 로 정해집니다.
key : 이 인수를 통해 정렬방식으로 함수를 사용할 수 있습니다. lamba의 사용이 가능합니다.
'''

na = np.nan
data = [[-3,'A',17],
        [na,'D',31],
        [ 7,'D',-8],
        [15,'Z', 3],
        [ 0, na,-7]]
col = ['col1','col2','col3']
row = ['row1','row2','row3','row4','row5']
df = pd.DataFrame(data = data, index = row, columns= col)
print(df)

print(df.sort_values(by='col3')) # by는 기준 레이블 정의

print(df.sort_values(by=['col2','col3'])) # list 형태로 전달이 되면 먼저 앞 기준값으로 정령을 하고, 동일한 값인 경우 뒤 정렬 기준에 따라 정렬된다.
print(df.sort_values(by='col3',axis=0)) # axis 축 기준, 0: index / 1: columns
print(df.sort_values(by='row5',axis=1)) # 현재 만든 DataFrame의 row 는 숫자, 문자 혼용으로 오류 발생

print('=========== 결측값 =======================')
print(df.sort_values(by='col1',na_position='last')) # 결측값 : 데이터가 없는 값, 의 위치를 지정
print(df.sort_values(by='col2',na_position='first')) # 정렬 기준이 되는 레이블에서 결측값의 위치를 지정한다.


print('============== ignore_index ===============')
print(df.sort_values(by='col3'))
print(df.sort_values(by='col3', ignore_index=True)) # 기존 index 값을 사용하지 않고, 정렬된 순서의 인덱스를 0부터 시작하는 정수가 채워진다. 

print('=========== key ===============')
print(df.sort_values(by="col2", key=lambda col: col.str.lower())) # key 를 이용하여 정렬에 함수 이용가능 (lambda식 사용.)

print('================= inplace ====================')
df.sort_values(by='col3',inplace=True) # 원본 데이터를 사용할지 복사복을 만들어 반환 할지의 여부 선택 
'''
개요

sort_index 메서드는 인덱스를 기준으로 레이블을 정렬하는 메서드입니다.

사용법

기본 사용법
df.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True, ignore_index=False, key=None)
axis : {0 : index / 1: columns} 정렬할 레이블입니다. 0이면 행, 1이면 열을 기준으로 정렬합니다.
level : multi index의 경우 정렬을 진행할 level입니다.
ascending : 오름차순으로할지 여부 입니다. 기본은 True로 오름차순입니다.
inplace : 원본을 대체할지 여부입니다. True일 경우 원본을 대체하게 됩니다.
kind : 알고리즘 모드 입니다. 모드는 총 4종으로 quicksort, mergesort, heapsort, stable이 있는데,
속도와 효율성의 차이를 갖습니다. 기본적으로 quicksort이며, 자세한건 numpy doc에서 확인 가능합니다.
na_position : {first / last} Na값의 위치입니다. 기본값은 last로 정렬시 맨 뒤에 위치합니다.
sort_remaining : multi index의 경우 다른 레벨에 대해서도 정렬을할지 여부입니다. True로 할 경우
한 레벨에 대한 정렬이 완료되면, 다른 레벨도 정렬합니다.
ignore_index : 인덱스의 무시 여부입니다. True일 경우 인덱스의 순서와 상관없이 0,1,2,... 로 정해집니다.
'''

na = np.nan
index_tuples = [('row1', 'val1'), ('row1', 'val2'), ('row3', 'val3'), ('row3', 'val1'), ('row3', 'val2'), ('row2', 'val5'),('row2', 'val2')] 
values = [ [1,2,3], [4,na,6], [7,8,9], [na,11,12], [13,14,15], [16,17,18], [19,20,21]]
index = pd.MultiIndex.from_tuples(index_tuples) # 인덱스 설정
df = pd.DataFrame(values, columns=['col4', 'col1', 'col2'], index = index)
print(df)


# level의 지정
# level 은 DataFrame를 만들 때 multi index로 만든 레벨을 기준으로 정렬을 하겠다.
print('========= level 지정 =================')
print(df.sort_index(axis=0, level=0))
print(df.sort_index(axis=0, level=1))


# level별 ascending의 병용
print('=============== level & ascending =================')
print(df.sort_index(axis=0, level=[1,0],ascending=[False,True])) # level, ascending 값을 list 형태로 전달 하면서 각 level 의  정렬방식을 다르게 가져간다.

print(df.sort_index(axis=0, sort_remaining=True)) # level 별로 순차적으로 정령 진행,
print(df.sort_index(axis=0, sort_remaining=False, level=1)) # level 을 지정하면 레벨만 정령 나머지 정렬 x (sort_remaining: False인 경우)

