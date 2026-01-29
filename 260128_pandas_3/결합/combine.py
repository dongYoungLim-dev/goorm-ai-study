import pandas as pd
import numpy as np


'''
combine 메서드는 두 pandas 객체를 func함수를 이용하여 결합하는 메서드입니다.

기본 사용법
self.combine(other, func, fill_value=None, overwrite=True)
other : 결합 할 DataFrame객체 입니다.
func : 결합에 이용할 함수 입니다.
fill_value : 결합하기전 Na의 값을 이 값으로 대체합니다.
overwrite : other에 존재하지 않는 self의 열의 값을 NaN으로 대체합니다.
'''

n = np.nan
col = ['col1', 'col2', 'col3']
row = ['row1', 'row2', 'row3']
data1 = [[1, 2, 3], [n, 8, 2], [2, 6, 7]]
data2 = [[7, 2, 3], [2, 4, 2], [3, 1, 5]]

df1 = pd.DataFrame(data1, row, col)
df2 = pd.DataFrame(data2, row, col)

print('=========== 기본 Data Frame ==============')
print(df1)
print(df2)

print('=========== func = np maximum 사용하여 큰 값으로 결합 ======')
print(df1.combine(df2, np.maximum)) # 기본 사용법의 combine 함수의 인자의 전달 값으로 순서에 맞게 전달하는 경우
print(df1.combine(other=df2, func=np.maximum)) # combine 함수의 인자에 직접 대입하는 형태로도 동일한 결과를 얻을 수 있다.


print('============= fill_value 사용 ================')
print(df1.combine(df2, np.maximum, fill_value=9)) # 결측치의 기본값을 설정 nan 이 설정한 9로 표시된다.


print('============== overwrite 사용 =================')
col3 = ['col1','col2']
row3 = ['row1','row2']
data3 = [[1,2],
         [3,4]]
df3 = pd.DataFrame(data3, row3, col3)
print('=== 기본 df3 데이터 ===')
print(df3)

print('# overwrite Ture, False 비교')
print(df1.combine(df3, np.maximum, overwrite=False)) # overwrite 는 열에만 적용된다.
print(df1.combine(df3, np.maximum, overwrite=True)) # df1, df3 에 col1, col2는 둘다 존재하지만, col3 는 df1에만 존재 overwrite 는 열에만 적용이 되기때문에 col3 값만 overwrite 값에 영향을 받아 df1의 값이 표시 되거나 nan값이 표시 된다.


