import numpy as np
import pandas as pd

'''
개요

join 메서드는 두 객체를 인덱스 기준으로 병합하는 메서드 입니다.

사용법

self.join(other, on=None, how='left', lsuffix='', rsuffix='', sort=False)
other : self와 합칠 객체 입니다.
on : self의 열이나 인덱스 중에서 other의 어떤 열을 기준으로 결합할지 입니다.
즉, other의 (인덱스 기준이 아닌) 열 기준으로 결합할 때 on인수를 사용합니다.
how : {left : self기준 / right : other기준 / inner : 교집합 / outer : 합집합} 출력할 인덱스의 기준입니다.
lsuffix / rsffix : 이름이 중복되는 열이 있을 때 그 열에 추가로 붙일 접미사입니다.
lsuffix는 self의 열에 붙을 접미사고, rsuffix는 other의 열에 붙을 접미사입니다.
sort : 출력되는 데이터의 index를 사전적으로 정렬할지 여부입니다.
'''


df1 = pd.DataFrame({'col1':[1, 2, 3]}, index=['row3', 'row2', 'row1'])
df2 = pd.DataFrame({'col2':[13, 14]}, index=['row4', 'row3'])
df3 = pd.DataFrame({'col1':[23, 24]}, index=['row4', 'row3'])
df4 = pd.DataFrame({'col1':[23, 24]}, index=['row4', 'row3'])
df5 = pd.DataFrame({'col1':[23, 24]}, index=['row4', 'row3'])


print('======== 기본 DataFrame ==========')
print(df1)
print(df2)
print(df3)




print('========= how ============')
print(df1.join(df2, how='left')) # left df1 을 기준으로 병합(df1에 없는 행은 출력되지 않는다.)
print(df1.join(df2, how='right')) # right df2 를 기준으로 병합(df2dp 없는 행은 출력되지 않는다.)
print(df1.join(df2, how='outer')) # outer df1, df2 합집합을 기준으로 병합(df1과 df2에서 각각 얿는 행을 nan으로 채워지면서 병합된다.)
print(df1.join(df2, how='inner')) # inner df1, df2 교집합을 기준으로 병합(df1과 df2에 모두 존재하는 행만 출력된다.)


print('============ sort ===============')
print(df1.join(df2,how='left'))
print(df1.join(df2, how='left', sort=False)) # index 기준으로 정렬되지 않는다.
print(df1.join(df2, how='left', sort=True)) # index 기준으로 정력된다.



print('============ lsuffix, rsuffix ============')
print(df1.join(df3, how='outer', lsuffix="_left", rsuffix='_right')) # 중복되는 name에 각각의 이름표를 설정해준다.


print('============ 여러 DataFrame 한 번에 join ============')
# 방법 1: 리스트로 여러 DataFrame을 한 번에 join (중복 열 이름이 없을 때만 가능)
# df2는 'col2'만 있으므로 문제없지만, df3, df4, df5는 모두 'col1'이 있어서 에러 발생
# print(df1.join([df2, df3, df4, df5], how='outer'))  # 에러: 중복 열 이름

# 방법 2: 체이닝 방식으로 각각 suffix 사용 (중복 열 이름이 있을 때 권장)
print(df1.join(df2, how='outer')
      .join(df3, how='outer', rsuffix='_df3')
      .join(df4, how='outer', rsuffix='_df4')
      .join(df5, how='outer', rsuffix='_df5'))

# 방법 3: 열 이름을 미리 변경한 후 리스트로 join
df3_renamed = df3.rename(columns={'col1': 'col1_df3'})
df4_renamed = df4.rename(columns={'col1': 'col1_df4'})
df5_renamed = df5.rename(columns={'col1': 'col1_df5'})
print(df1.join([df2, df3_renamed, df4_renamed, df5_renamed], how='outer'))



print('============ set_index ==============')

df6 = pd.DataFrame({'IDX': ['A','B','C'], 'col1':[1, 2, 3]})
df7 = pd.DataFrame({'IDX':['C','D'], 'col2': [13,14]})


print(df6.set_index('IDX').join(df7.set_index('IDX')))
print(df6.join(df7.set_index('IDX'), on='IDX'))