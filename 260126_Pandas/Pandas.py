import pandas as pd
import numpy as np

# Pandas.Series

'''
시리즈(Series)
1차원 배열의 형태를 가진 데이터 구조, 각각의 데이터의 고유한 인덱스 부여.
기본 구조 : s = pd.Series(data, index=index_data)
'''

s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
print(s)

print(s.index)
print(s.values) # values 출력 결과 배열과 같아 보이지만 ','로 구분하지 않고, ' '공백으로 구분 이는 pandas는 numpy 배열읍 반환하기 때문이다.
print(s.dtype) # series data type 확인


s1 = pd.Series({'a':1, 'b':2, 'c':3, 'D':4}) # Series 데이터 구조를 만들때 dictionary 데이터를 사용하면 index 옵션을 사용하지 않고, dict key = index, value = value 가 된다.
print(s1)
print(s1[['a', 'c']]) # Series 데이터는 인덱스트 지정하여 값을 출력할 수 있다.
print(f"s1 == 'D' = {s1[s1 == 'D']}") 

s2 = pd.Series([1, 2, 3, 4, 5])
print(s2)
print(s2.index)
print(s2[s2 > 2]) # Series 데이터는 인덱스를 지정하지 않으면 자동으로 인덱싱이 되는데 이 경우 조건을 걸어 원하는 데이터를 출력할 수 있다.
print(s2[[1, 2]]) 
# Pandas.DataFrame

'''
list, tuple, dictionary, Series 형태를 주로 전달한다.
기본 구조 : df = pd.DataFrame(data, index=index_data, columns=columns_data)
index = 데이터의 행 이름을 지정하는 데이터,
columns = 데이터의 열 이름을 지정하는 데이터
index, columns 값을 지정하지 않으면 0부터 시작하는 정수가 자동으로 삽입된다.
'''
data_dict = {
    '이름': ['소라', '창훈', '영미'],
    '나이': [25, 30, 35],
    '거주지': ['인천', '순천', '동해']
}

df_dict = pd.DataFrame(data_dict) # DataFrame 에서 columns 값을 지정하지 않고, dictionary 를 전달하면 dict key 값이 columns 값으로 설정되고, index 값을 0부터 시작하는 정수로 채워진다.
print(df_dict)
print(df_dict.columns) # Series 와 마찬가지로, index, values, dtype 을 따로 가져와 확인이 가능하다. 추가로 columns를 따로 가져 올 수 있다.


# Pandas.DataFrame (add, radd)

'''
add함수는 DataFrame에 다른 df, Series, 스칼라 등 데이터를 더하는 메서드
기본 사용법
other : 더할 값 (다른 df, Series, 스칼라 등)
axis: 더할 레이블 0: 행, 1: 열
level: axis 에서 지정한 행 또는 열 기준으로 몇번째 부터 진행할건지
fill_value: NaN 값들의 누락요소, 빈값을 대체하는 값 설정
'''
# TODO: 스칼라에 대한 정확한 이해 집고 넘어가기 

data = [[1,10,100],[2,20,200],[3,30,300]]
col = ['col1','col2','col3']
row = ['row1','row2','row3']
df = pd.DataFrame(data=data,index=row,columns=col)
print(df)


# 스칼라
result = df.add(1) # 행과 열 전체에 +1 한 값을 출력한다.
# 조금더 직관적으로 생각하면 data에 담긴 이중 list를 하나의 배열이라고 생각하고
# [1, 10, 100 ... ] => 여기에 각 index 에 +1 값을 보여준다.
print(result)

result2 = df + 1 # 위와 동일한 결과를 보여 준다. 
print(result2)

# 다른 df 
data2  = [[3],[4],[5]]
df2 = pd.DataFrame(data=data2,index=['row1','row2','row3'],columns=['col1'])
print(df2)

result3 = df.add(df2) 
# df, df2는 서로 데이터가 다르기 때문에 비어있는 값은 NaN 으로 표시가 된다.
print(result3)


result4 = df.add(df2, fill_value=0) # 비어있는 값을 0으로 채우고, 두 DataFrame 를 더하기 떼문에 NaN 값이 나오지 않고, 계산된값이 나온다.

print(result4)

print("="*40)
# Pandas.DataFrame (sub, rsub)

'''
add 와 마찬가지로 다른 df, Series, 스칼라 데이터를 전달하여 빼는 메서드 입니다.
'''
data3 = [[1,10,100],[2,20,200],[3,30,300]]
col3 = ['col1','col2','col3']
row3 = ['row1','row2','row3']
df3 = pd.DataFrame(data=data3,index=row3,columns=col3)

print(df3)

print(df3.sub(1))
print(df3 - 1)
# 위 두 값은 동일한 결과물을 출력한다.

data4  = [[3],[4],[5]]
df4 = pd.DataFrame(data=data4,index=['row1','row2','row3'],columns=['col1'])
print(df4)

result4 = df3.sub(df4)
print(result4)


result4_1 = df3.sub(df4, fill_value=0)
print(result4_1)

print("="*60)
# (mul, rmul)
'''
add,sub와 마찬가지로 값을 곱하는 메서드
기본 사용법
df.mul(other, axis='columns', level=None, fill_value=None)
other : 데이터프레임이나, Series, 스칼라 등 데이터가 올 수 있습니다. 곱할 값입니다.
axis : 곱할 레이블을 설정합니다. 0은 행(index), 1은 열 입니다. ※Series일 경우 Index와 일치시킬 축
level : multiIndex에서 계산할 Index의 레벨입니다.
fill_value : NaN 값등의 누락 요소를 계산 전에 이 값으로 대체합니다.
'''
data5 = [[1,10,100],[2,20,200],[3,30,300]]
col5 = ['col1','col2','col3']
row5 = ['row1','row2','row3']
df5 = pd.DataFrame(data=data5,index=row5,columns=col5)
print(df5)


print(df5.mul(2))
print(df5 * 2)
# 위 두개의 결과는 동일하게 출력됩니다.

data5_1 = [[3],[4],[5]]
df5_1 = pd.DataFrame(data=data5_1,index=['row1','row2','row3'],columns=['col1'])
print(df5_1)

print(df5.mul(df5_1))
print(df5.mul(df5_1, fill_value=0))

# (div, rdiv)

data6 = [[1, 10, 100], [2, 20, 200], [3, 30, 300]]
col6 = ['col1', 'col2', 'col3']
row6 = ['row1', 'row2', 'row3']
df6 = pd.DataFrame(data=data6, index=row6, columns=col6)
print(df6)

print(df6.div(2))
print(df6/2)

data6_1 = [[0], [1], [3]]
df6_1 = pd.DataFrame(data=data2,index=['row1','row2','row3'],columns=['col1'])
print(df6_1)

print(df6.div(df6_1))
print(df6.div(df6_1, fill_value=1))


print('='*60)

# (mod, rmod)
'''
데이터를 나누고 나머지는 반환하는 메서드
'''

mod_data = [[1,2,3],[4,5,6],[7,8,9]]
mod_col = ['col1','col2','col3']
mod_row = ['row1','row2','row3']

mod_df = pd.DataFrame(data=mod_data,index=mod_row,columns=mod_col)
print(mod_df)


print(mod_df.mod(7))

mod_data2  = [[2],[3],[5]]
mod_df2 = pd.DataFrame(data=mod_data2,index=['row1','row2','row3'],columns=['col1'])
print(mod_df2)

print(mod_df.mod(mod_df2))
print(mod_df.mod(mod_df2, fill_value=1))

print('='*60)
# (pow, rpow)
'''
데이터를 거듭제곱 한다. 
'''
pow_data = [[1,2,3],[4,5,6],[7,8,9]]
pow_col = ['col1','col2','col3']
pow_row = ['row1','row2','row3']
pow_df = pd.DataFrame(data=pow_data,index=pow_row,columns=pow_col)
print(pow_df)



print(pow_df.pow(3))
print(pow_df ** 3)
# 위 두개의 print문은 동일하게 출력을 한다.

pow_data2  = [[0],[3],[5]]
pow_df2 = pd.DataFrame(data=pow_data2,index=['row1','row2','row3'],columns=['col1'])

print(pow_df2)


print(pow_df.pow(pow_df2))
print(pow_df.pow(pow_df2, fill_value=0))

# (dot) 행렬곱

dot_col = ['col1','col2']
dot_row = ['row1','row2']
dot_data1 = [[1,2],[3,4]]
dot_data2 = [[5,6],[7,8]]
dot_df1 = pd.DataFrame(data=dot_data1)
dot_df2 = pd.DataFrame(data=dot_data2)
print(dot_df1)
print(dot_df2)


dot_df3 = dot_df1.dot(dot_df2)
print(dot_df3)



# (round) 반올림
'''
round 함수는 DataFrame 객체 내의 요소를 반올림하는 메소드
기본 사용법
df(decimals(소수)=0, args, kwargs)

# 10의 n승 -1 자리에서 판단하여 5이상이면 10의 n승 자리 올림처리
# 10의 n승 -1 자이의 숫자가 5 일 경우, 10의 n승 자리가 짝수가 되도록 움직인가. python에서는
'''
round_col = ['col1','col2','col3']
round_row = ['row1','row2','row3']
round_data = np.random.rand(3,3)*100
round_df = pd.DataFrame(data=round_data, index=round_row, columns=round_col)
print(round_df)

# decimals = 0
print(round_df.round(0))
# decimals > 0
print(round_df.round(1)) # 소수 첫째 자리 까지 반올림
print(round_df.round(2)) # 소수 두번째 자리 까지 반올림
# decimals < 0
print(round_df.round(-1)) # 양수인 경우 10의 n승 자리까지 반올림
print(round_df.round(-2))

# print(1756.56.round(-3)) -> 결과 2000
# round(-1) -> 10의 1승 -> 10자리 까지 
# 10의 2승 -> 100
# 10의 3승 -> 1000

# (sum) 합계
'''
df.sum(axis=None, skipna=None, level=None, numeric_only=None, min_count=0, kwargs)

axis : { 0 : 행 / 1 : 열} 더할 레이블을 선택합니다.
skipna : {True or False} NaN가 존재할 경우 무시할지의 여부입니다. 기본값은 True입니다.
level : Multi Index일 경우 레벨을 설정합니다.
numeric_only : 숫자 데이터만 사용할지의 여부 입니다.
min_count : 계산에 필요한 숫자의 최소 갯수입니다.
'''

sum_col = ['col1','col2','col3']
sum_row = ['row1','row2','row3']
sum_data = [[1,2,3],[4,5,6],[7,np.nan,9]]
sum_df = pd.DataFrame(data=sum_data,index=sum_row,columns=sum_col)
print(sum_df)

print(sum_df.sum(axis=0))
print(sum_df.sum(axis=1))

print(sum_df.sum(axis=0, skipna=False))
print(sum_df.sum(axis=0, min_count=3)) # min_count -> 계산이 필요한 숫자의 최소 갯수 의미 skipna=True 여도 최소가 3개이기 때문에 nan 표시

# (prod, product) 곱
'''
df.prod(axis=None, skipna=None, level=None, numeric_only=None, min_count=0, kwargs)
axis : { 0 : 행 / 1 : 열} 곱할 레이블을 선택합니다.
skipna : {True or False} NaN가 존재할 경우 무시할지의 여부입니다. 기본값은 True입니다.
level : Multi Index일 경우 레벨을 설정합니다.
numeric_only : 숫자 데이터만 사용할지의 여부 입니다.
min_count : 계산에 필요한 숫자의 최소 갯수입니다.
'''
prod_col = ['col1','col2','col3']
prod_row = ['row1','row2','row3']
prod_data = [[1,2,3],[4,5,6],[7,np.nan,9]]
prod_df = pd.DataFrame(data=prod_data,index=prod_row,columns=prod_col)
print(prod_df)

print(prod_df.prod(axis=0))
print(prod_df.prod(axis=1))

print(prod_df.prod(axis=0, skipna=False))
print(prod_df.prod(axis=0, min_count=3))

# (abs) 절대값
'''
df.abs( )
숫자의 경우 절댓값을 반환하며, 복소수의 경우 복소수의 크기가 반환됩니다.
※ 복소수가 a+bj인 경우 복소수의크기
NaN의 경우는 NaN을 그대로 출력합니다.
'''

# TODO: 복소수 학습.

abs_col = ['col1','col2','col3']
abs_row = ['row1','row2','row3']
abs_data = [[-1,2,-3.5],[4,-5.5, 3+4j],[7,np.nan,0]]
abs_df = pd.DataFrame(data=abs_data,index=abs_row,columns=abs_col)
print(abs_df)

print(abs_df.abs( ))

# (transpose, T) 전치
'''
transpose 메서드는 Dataframe객체를 전치 하는 메서드입니다.
만약 (n,m)짜리 DataFrame이라면 (0,0) 부터 (n,m)을 연결하는 대각선을 중심으로 뒤집는것과 같습니다.
※ T 메서드는 transpose 메서드와 동일합니다.

기본사용법
copy : 사본을 반환할지 여부입니다. 여러 dtype으로 이루어진 경우 자동으로 True가 됩니다.
'''
t_col = ['col1','col2','col3']
t_row = ['row1','row2','row3','row4']
t_data = [['A',1,2],['B',3,4],['C',5,6],['D',7,8]]
t_df = pd.DataFrame(data=t_data,index=t_row,columns=t_col)
print(t_df)


print(t_df.transpose())

# (rank) 순위
'''
rank 메서드는 축에 대해서 순위를 매기는 메서드 입니다. 동일 순위일 경우 평균을 반환합니다.

df.rank(axis=0, method='average', numeric_only=None, na_option='keep', ascending=True, pct=False)
axis : {0 : index / 1 : columns} 순위를 매길 레이블입니다.
method : {'average' / 'min' / 'max' / 'first' / 'dense'} 동순위 일때 처리 방법입니다.
average는 평균, min은 낮은순위, max는 높은순위, first는 나타나는순서대로
dense의 경우는 min과 같지만 그룹간 순위는 항상 1씩 증가합니다.
numeric_only : {True / False} 숫자만 순위를 매길지 여부 입니다.
na_option : {'keep' / 'top' / 'bottom'} NaN값의 처리 방법입니다.
keep의 경우 NaN순위 할당, top의 경우 낮은순위 할당, bottom의 경우 높은 순위를 할당합니다.
ascending : {True / False} 오름차순으로 할지의 여부 입니다.
pct : {True / False} 순위를 백분위수형식으로 할지 여부입니다.
'''

rank_data = [[5],[5],[pd.NA],[3],[-3.1],[5],[0.4],[6.7],[3]]
rank_row = ['A★','B★','C','D☆','E','F★','G','H','I☆']
rank_df = pd.DataFrame(data=rank_data, index=rank_row, columns=['Value'])
print(rank_df)

rank_df['average']=rank_df['Value'].rank(method='average')
rank_df['min']=rank_df['Value'].rank(method='min')
rank_df['max']=rank_df['Value'].rank(method='max')
rank_df['first']=rank_df['Value'].rank(method='first')
rank_df['dense']=rank_df['Value'].rank(method='dense')
print(rank_df)

rank_df['keep']=rank_df['Value'].rank(na_option='keep')
rank_df['top']=rank_df['Value'].rank(na_option='top')
rank_df['bottom']=rank_df['Value'].rank(na_option='bottom')
rank_df['pct']=rank_df['Value'].rank(pct=True)
print(rank_df)


# (diff) 차이[이산]
'''
기본 사용법
※ 자세한 내용을 아래 예시를 참고 바랍니다.
df.diff(periods=1, axis=0)
axis : 비교할 축을 지정합니다. axis=0 인 경우 행끼리 비교하고 axis=1인 경우 열 끼리 비교합니다.
periods : 비교할 간격을 지정합니다. 기본은 +1로 바로 이전 값과 비교합니다.
'''

diff_a = [1,2,3,4,5,6,7,8]
diff_b = [1,2,4,8,16,32,64,128]
diff_c = [8,7,6,5,4,3,2,1]
diff_data = {"col1":diff_a,"col2":diff_b,"col3":diff_c}
diff_df = pd.DataFrame(diff_data)
print(diff_df)


# axis=0: 행 - 바로전 행, 값을 출력
print(diff_df.diff(axis=0))
# axis=1: 열 - 바로전 열, 값을 출력
print(diff_df.diff(axis=1))

# periods: default = +1, 기본 값이면 바로 이전 값과의 차이를 출력
print(diff_df.diff(periods=3)) # +3 으로 이전 3칸값과의 차이를 출력


# (pct_change) 차이[백분률]
'''
기본 사용법 (pandas 2.0+)
※ 자세한 내용을 아래 예시를 참고 바랍니다.
df.pct_change(periods=1, freq=None, **kwargs)

주요 파라미터:
- periods : 비교할 간격을 지정합니다. 기본은 +1로 바로 이전 값과 비교합니다.
- freq : 시계열 API에서 사용할 증분을 지정합니다. (예: 'ME' 또는 BDay())

⚠️ 주의사항:
- pandas 2.0 이상에서는 fill_method와 limit 파라미터가 제거되었습니다.
- 결측치 처리는 pct_change() 호출 전에 ffill() 또는 bfill() 메서드를 사용해야 합니다.

작동 방법은 기본적으로 다음 식을 의미한다 : (다음행 - 현재행)÷현재행
'''
pct_a = [1,1,4,4,1,1]
pct_b = [1,2,4,8,16,32]
pct_c = [1,np.nan,np.nan,np.nan,16,64]
pct_data = {"col1":pct_a,"col2":pct_b,"col3":pct_c}
pct_df = pd.DataFrame(pct_data)
print(pct_df)


print(pct_df.pct_change())

# TODO: 결측치 학습하기
# pandas 2.0 이상에서는 fill_method와 limit 파라미터가 제거되었습니다.
# 결측치 처리는 pct_change() 호출 전에 별도로 처리해야 합니다.

# 구 버전 방식 (pandas 1.x 이하)
# print(pct_df.pct_change(fill_method="bfill"))  # ❌ 더 이상 사용 불가
# print(pct_df.pct_change(limit=2))  # ❌ 더 이상 사용 불가

# 신규 버전 방식 (pandas 2.0+)
# 방법 1: ffill() 사용 (앞의 값으로 채움)
print(pct_df.ffill().pct_change())  # ✅ 앞의 유효한 값으로 결측치를 채운 후 백분율 변화 계산

# 방법 2: bfill() 사용 (뒤의 값으로 채움)
print(pct_df.bfill().pct_change())  # ✅ 뒤의 유효한 값으로 결측치를 채운 후 백분율 변화 계산

# 방법 3: limit과 함께 사용
print(pct_df.ffill(limit=2).pct_change())  # ✅ 최대 2개까지만 앞의 값으로 채움

# 방법 4: 특정 값으로 채우기
print(pct_df.fillna(0).pct_change())  # ✅ 결측치를 0으로 채운 후 백분율 변화 계산

# (expanding) 누적계산
'''
expanding 메서드는 누적 계산(expanding window)을 수행하는 메서드입니다.
시간이 지날수록 윈도우 크기가 증가하며, 모든 이전 데이터를 포함하여 계산합니다.

기본 사용법
df.expanding(min_periods=1, method='single', axis=None)
min_periods : 계산에 필요한 최소 관측값 수입니다. 기본값은 1입니다.
method : {'single' / 'table'} 실행 방법을 지정합니다. 'single'은 각 열/행별로, 'table'은 전체 객체에 대해 실행합니다.

주요 집계 함수:
- sum() : 누적 합계
- mean() : 누적 평균
- max() : 누적 최대값
- min() : 누적 최소값
- std() : 누적 표준편차
- var() : 누적 분산
- count() : 누적 개수
'''

expanding_data = [[1, 10], [2, 20], [3, 30], [4, 40], [5, 50]]
expanding_col = ['col1', 'col2']
expanding_row = ['row1', 'row2', 'row3', 'row4', 'row5']
expanding_df = pd.DataFrame(data=expanding_data, index=expanding_row, columns=expanding_col)
print("원본 데이터:")
print(expanding_df)

print("\n누적 합계 (expanding().sum()):")
print(expanding_df.expanding().sum())  # 각 행까지의 누적 합계

print("\n누적 평균 (expanding().mean()):")
print(expanding_df.expanding().mean())  # 각 행까지의 누적 평균

print("\n누적 최대값 (expanding().max()):")
print(expanding_df.expanding().max())  # 각 행까지의 누적 최대값

print("\nmin_periods=3 설정 (최소 3개 관측값 필요):")
print(expanding_df.expanding(min_periods=3).sum())  # 처음 2개는 NaN, 3번째부터 계산

print("\n누적 표준편차 (expanding().std()):")
print(expanding_df.expanding().std())

print("="*60)

# (rolling) 기간이동 계산
'''
rolling 메서드는 고정 크기 윈도우를 이동시키며 계산하는 메서드입니다.
지정한 기간(window)만큼의 데이터를 사용하여 집계 함수를 계산합니다.

기본 사용법
df.rolling(window, min_periods=None, center=False, win_type=None, on=None, axis=None, closed=None, method='single')
window : 윈도우 크기 (이동할 기간의 크기)
min_periods : 계산에 필요한 최소 관측값 수입니다. 기본값은 window와 동일합니다.
center : 윈도우를 중앙에 배치할지 여부입니다. False면 현재 행을 기준으로 이전 값들을 사용합니다.
win_type : 윈도우 타입을 지정합니다. (예: 'triang', 'blackman', 'hamming' 등)
closed : 윈도우의 양쪽 끝을 포함할지 여부입니다. {'right', 'left', 'both', 'neither'}

주요 집계 함수:
- sum() : 이동 합계
- mean() : 이동 평균
- max() : 이동 최대값
- min() : 이동 최소값
- std() : 이동 표준편차
- var() : 이동 분산
- count() : 이동 개수
'''

rolling_data = [[1, 10], [2, 20], [3, 30], [4, 40], [5, 50], [6, 60], [7, 70]]
rolling_col = ['col1', 'col2']
rolling_row = ['row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7']
rolling_df = pd.DataFrame(data=rolling_data, index=rolling_row, columns=rolling_col)
print("원본 데이터:")
print(rolling_df)

print("\n3기간 이동 합계 (rolling(3).sum()):")
print(rolling_df.rolling(window=3).sum())  # 3개 행씩 묶어서 합계 계산

print("\n3기간 이동 평균 (rolling(3).mean()):")
print(rolling_df.rolling(window=3).mean())  # 3개 행씩 묶어서 평균 계산

print("\n3기간 이동 최대값 (rolling(3).max()):")
print(rolling_df.rolling(window=3).max())  # 3개 행씩 묶어서 최대값 계산

print("\nmin_periods=1 설정 (최소 1개 관측값만 있어도 계산):")
print(rolling_df.rolling(window=3, min_periods=1).sum())  # 처음 2개도 계산됨

print("\ncenter=True 설정 (윈도우를 중앙에 배치):")
print(rolling_df.rolling(window=3, center=True).mean())  # 현재 행을 중심으로 앞뒤 값 사용

print("\n5기간 이동 평균 (rolling(5).mean()):")
print(rolling_df.rolling(window=5).mean())  # 5개 행씩 묶어서 평균 계산

print("\n3기간 이동 표준편차 (rolling(3).std()):")
print(rolling_df.rolling(window=3).std())  # 3개 행씩 묶어서 표준편차 계산
