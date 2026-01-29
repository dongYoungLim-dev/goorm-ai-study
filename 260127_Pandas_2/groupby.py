import numpy as np
import pandas as pd

# 그룹화 계산 (groupby)
'''
기본 사용법
※ 자세한 내용은 아래 예시를 참고 바랍니다.
df.groupby(by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=NoDefault.no_default, observed=False, dropna=True)
by : 그룹화할 내용입니다. 함수, 축, 리스트 등등이 올 수 있습니다.
axis : 그룹화를 적용할 축입니다.
level : 멀티 인덱스의 경우 레벨을 지정할 수 있습니다.
as_index : 그룹화할 내용을 인덱스로 할지 여부입니다. False이면 기존 인덱스가 유지됩니다.
sort : 그룹키를 정렬할지 여부입니다.
group_keys : apply메서드 사용시 결과에따라 그룹화 대상인 열이 인덱스와 중복(group key)이 될 수 있습니다. 이 때, group_keys=False로 인덱스를 기본값으로 지정할 수 있습니다.
squeeze : 결과가 1행 or 1열짜리 데이터일 경우 Series로, 1행&1열 짜리 데이터일 경우 스칼라로 출력합니다.
observed : Categorical로 그룹화 할 경우 Categorical 그룹퍼에 의해 관찰된 값만 표시할 지 여부입니다.
dropna : 결측값을 계산에서 제외할지 여부입니다.
'''


idx=['A','A','B','B','B','C','C','C','D','D','D','D','E','E','E']
col=['col1','col2','col3']
data = np.random.randint(0,9,(15,3))
df = pd.DataFrame(data=data, index=idx, columns=col).reset_index()
print(df)

print('========= 기본 groupby ===============')
print(df.groupby('index')) # 동일한 index 기준으로 group화 진행ㅒ 
print('================ mean() ================')
print(df.groupby('index').mean()) # 평균치 계산

print('=========== agg() ===============')
print(df.groupby('index').count())
print(df.groupby('index').agg(['sum','mean'])) # agg 메서드를 이용하여 여러 연산을 수행 가능하다.


print('================ group_keys =================')
'''
group_keys 인수의 사용
apply 메서드를 이용해 groupby연산을 수행할 경우, groupkey가 설정되기 때문에 때에따라 컬럼과 인덱스가 중복될 수 있습니다. 이 때 group_keys=False를 통해 기본 인덱스로 출력이 가능합니다.
'''
def top (df,n=2,col='col1'):
    return df.sort_values(by=col)[-n:] #상위 n개 열을 반환하는 함수 top 생성
print(df.groupby('index').apply(top)) # 적용전
print(df.groupby('index',group_keys=False).apply(top)) # 그룹 인덱스를 적용하지 않고, 원래 인덱스를 따라 인덱스가 설정 됩니다.


print('================ observed 인수 사용 ================')
df_cat = pd.Categorical(df['index'], categories=['A','B','C','D','E','F']) # df의 index열에 대해서 A,B,C,D,E,F 로 Categorical을 하여 df_cat 생성
print(df_cat)

print(f"{df['col1'].groupby(df_cat).count()}")
print(df['col1'].groupby(df_cat,observed=False).count()) # 그룹화 진행시 그룹 열에 있지 않는 값을 포함하게 되면, 해당 값의 표시 여부를 선택

print('=============== as_index ==================')
print(df.groupby(['index'],as_index=False).sum()) # 열을 선택하여 그룹화 할 경우 해당 열이 index 다 되는데 as_index=False 하면, 기존 인덱스가 유지 된다.

print('=========== dropna =================== ')
df.loc[6,'index'] = np.nan
print(df)

print(df.groupby('index').sum()) # NaN을 계산에서 제외 시킨다.
print(df.groupby('index',dropna=False).sum()) # dropna 를 False 로 하게 되면 NaN 을 포함하여 계산하게 된다.

print('=============== multi index ===================')
idx = [['idx1','idx1','idx2','idx2','idx2'],['row1','row2','row1','row2','row3']]
col = ['col1','col2','col2']
data = np.random.randint(0,9,(5,3))
df = pd.DataFrame(data=data, index = idx, columns = col).rename_axis(index=['lv0','lv1'])
print(df)

print(df.groupby(level=1).sum()) # index level 기준으로 정렬을한다.
print(df.groupby(['lv1','lv0']).sum()) # level str로 지정, 여러개 지정// 지정시 순차적으로 groupby 된다.
print(df.groupby(['lv0','lv1']).sum()) # level str로 지정, 여러개 지정// 지정시 순차적으로 groupby 된다.
