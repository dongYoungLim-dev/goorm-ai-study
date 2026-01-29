import numpy as np
import pandas as pd


'''
개요

align메서드는 두 객체를 특정 기준들에 맞추어 정렬하는 메서드입니다.
두개의 데이터를 튜플 형태로 반환한다는것을 반드시 명심하시기 바랍니다.
인수들에 따라 다양한 구현이 가능하므로 아래 사용법을 참고 바랍니다.

사용법

self.align(other, join='outer', axis=None, level=None, copy=True, fill_value=None, method=None, limit=None, fill_axis=0, broadcast_axis=None)
other : self와 함께 정렬할 객체 입니다.
join : {inner / left / right / outer} 정렬 기준이 될 인덱스 입니다. inner이면 교집합, left면 self의 인덱스, right면 other의 인덱스, outer이면 합집합으로 인덱스를 사용합니다.
axis : {0 : index / 1 : columns} 정렬할 레이블입니다. 기본값으로 두 축 모두 정렬합니다.
level : multi index의 경우 실행할 수준(level)을 설정합니다.
copy : 사본을 생성할지의 여부입니다.
fill_value : 결측치를 어떤 값으로 채울지의 여부입니다. 기존 객체에 포함된 결측치의 경우는 바뀌지 않습니다.
method : {ffill / bfill} 결측치를 어떻게 채울지 여부입니다. ffill의 경우 위의값과 동일하게, bfill의 경우 아래 값과 동일하게 채웁니다.
limit : 결측치를 몇개나 채울지 여부입니다. limit에 설정된 갯수만큼만 결측치를 변경합니다.
fill_axis : {0 : index / 1 : columns} method와 limit를 가로로 적용할지 세로로 적용할지 여부입니다.
broadcast_axis : {0 : index / 1 : columns} 어느 축을 기준으로 브로드캐스트할지 여부입니다.
브로드캐스트란 서로 차원이 다른 두 객체에 대해서 저차원 데이터의 차원을 고차원 데이터에 맞추는 과정입니다.
자세한것은 [추후 brodcast항목 추가 예정] 에서 확인 가능합니다.
'''


n=np.nan
col1 = ['col1','col2','col3']
row1 = ['row1','row2','row3']
data1 = [[1,2,3],[5,6,7],[9,n,11]]

col2 = ['col2','col3','col4']
row2 = ['row3','row4','row5']
data2 = [[10,11,12],[14,n,16],[18,19,20]]

df1 = pd.DataFrame(data1,row1,col1)
df2 = pd.DataFrame(data2,row2,col2)

print(df1)
print(df2)

_df1, _df2 = df1.align(df2, join='outer')
print(_df1)
print('='*60)
print(_df2)
# print(df1.align(df2,join='outer')[0])
# print(df1.align(df2,join='outer')[1])