import numpy as np
import pandas as pd

'''
개요

update메서드는 DataFrame의 열을 other객체의 동일한 열의 값으로 덮어씌우는 메서드입니다.
반환값 없이 원본이 변경됩니다.

사용법

self.update(other, join='left', overwrite=True, filter_func=None, errors='ignore')
other : self에 덮어씌울 객체 입니다.
join : {left} 기준이 될 인덱스 입니다. left만 선택 가능하므로 무시해도됩니다.
overwrite : {True / False} 덮어씌울 방식입니다. True면 self의 모든 데이터에 other을 덮어씌웁니다.
False면 self에서 Na인 값에 대해서만 덮어씌우기를 진행합니다.
filter_func : 덮어씌울값을 함수로 정할 수 있습니다.
errors : {raise / ignore} raise일 경우 self와 other 모두 Na가 아닌 값이 있을경우 오류를 발생시킵니다.
'''

n = np.nan
print('=========== 기본 Data Frame =============')
df1 = pd.DataFrame({'A':[1,2,3],'B':[n,5,6]})
print(df1)
df2 = pd.DataFrame({'B':[24,n,26],'C':[37,38,39]})
print(df2)


df1.update(df2,overwrite=True)
print(df1)