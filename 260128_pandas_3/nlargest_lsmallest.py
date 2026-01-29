import pandas as pd


# nlargest # nsmallest
'''
기본 사용법
df.nlargest(n, columns, keep='first')
df.nsmallest(n, columns, keep='first')
n : 정렬 후 출력할 행의 수 입니다.
columns : 정렬의 기준이 될 열 입니다.
keep :{first, last, all} 동일한 값일경우 어느 행을 출력할지 정합니다. first면 위부터, last면 아래부터, all이면 모두 출력합니다.
'''

col = ['col1','col2','col3']
row = ['row3','row5','row1','row4','row2']
data = [[ 1, 21, 7],
        [ 2, 33, 3],
        [ 2,  7,97],
        [ 4, 56,31],
        [ 5, 18, 5]]

df = pd.DataFrame(data=data, index=row, columns=col)
print('======== 기본 Data Frame =============')
print(df)

print('=============== nlargest keep ==============')
print(df.nlargest(n=3,columns='col1',keep='last')) # keep은 중복되는 값이 포함된 행중 마지막 행을 표시 
print(df.nlargest(n=3,columns='col1',keep='first')) # 중복되는 값이 포함된 행중 첫번째 행을 표시
print(df.nlargest(n=3,columns='col1',keep='all')) # 중복되는 값이 포함된 모든행을 표시 한다.


print('=========== 여러 열을 동시에 고려하여 정렬 ==============')
print(df.nlargest(n=2, columns=['col1', 'col3']))





