import pandas as pd

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
# (sum) 합계
# (prod, product) 곱
# (abs) 절대값
# (transpose, T) 전치
# (rank) 순위
# (diff) 차이[이산]
# (pct_change) 차이[백분률]
# (expending) 누적계산
# (rolling) 기간이동 계산
