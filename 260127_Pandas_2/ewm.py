import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
지수 가중 함수(ewm) 

기본 사용법
※ 자세한 내용은 아래 예시를 참고 바랍니다.
df.ewm(com=None, span=None, halflife=None, alpha=None, min_periods=0, adjust=True, ignore_na=False, axis=0, times=None, method='single')

기본적으로 가중치를 결정하는 요소는 alpha 로 표기되는 평활계수(감쇠계수) 입니다. com / span / halflife를 통해 자동 계산하도록 하거나, alpha를 통해 직접 설정할 수 있습니다.

com : 질량중심 값으로 평활계수를 계산합니다. [ a = 1(1+com) ]
span : 계산 기간으로 평활계수를 계산합니다. [ a = 2/(span+1) ]
halflife : 반감기를 이용하여 평활계수를 계산합니다. [ a= e^(-ln(2) / halflife) ]
alpha : 평활계수를 직접 입력합니다. [ 0 < a ≤ 1 ]
min_periods : 계산을위한 최소 기간입니다.
adjust : 상대적 가중치의 불균형을 해소하기위해 조정계수로 나눌지의 여부입니다. 대체로 값이 많을수록 adjust를 하는것이 유리합니다.
ignore_na : 가중치를 계산할때 누락값을 무시할지 여부 입니다.

[x0, None, x1] 일때, 인 경우 ignore_na = False 이면 절대위치를 기반으로 하며,
x0와 x2의 가중치는 adjust = [ True인경우 (1-a)^2와 1 / False인 경우 (1-a)^2와 a ] 입니다.
[x0, None, x1] 일때, 인 경우 ignore_na = False 이면 절대위치를 기반으로 하며,
x0와 x2의 가중치는 adjust = [ True인경우 (1-a)와 1 / False인 경우 (1-a)와 a ] 입니다.

axis : 계산을 수행할 축 입니다.
times : 관찰에 해당하는 시간입니다. 단조증가 형태의 datetime64[ns] 형태여야합니다.
method : {single / table} 한 줄씩 계산할지(기본값) 아니면 numba engine을 사용해서 table단위로 계산할지 정할 수 있습니다.
numba 라이브러리를 import 해야하며 사용시 ewm(method='table').mean(engine='numba') 처럼 추가 메서드에 engine 설정을 해줘야합니다.
'''

data = {'val':[1,4,2,3,2,5,13,10,12,14,np.nan,16,12,20,22]}
df = pd.DataFrame(data).reset_index()
print(df)

df2 = df.assign(ewm=df['val'].ewm(alpha=0.3).mean()) # val열에 ewm 메서드적용 후 df에 추가
ax = df.plot(kind='bar',x='index',y='val') # ax에 df의 bar chart 생성
ax2= df2.plot(kind='line',x='index', y='ewm', color='red', ax=ax) # ax2에 df2의 line chart 생성후 ax에 추가
# plt.show() # 그래프 출력


df2 = df.assign(ewm=df['val'].ewm(alpha=0.3).mean()) # val열에 ewm 메서드적용 후 df에 추가
ax = df.plot(kind='bar',x='index',y='val') # ax에 df의 bar chart 생성
ax2= df2.plot(kind='line',x='index', y='ewm', color='red', ax=ax) # ax2에 df2의 line chart 생성후 ax에 추가
# plt.show() # 그래프 출력

'''
alpha에 따른 차이
alpha는 평활계수로써, 자동 계산이 가능하지만, alpha 인수를 직접 입력하여 설정이 가능합니다.
alpha가 클수록 더 큰 변화에 민감하며, alpha가 작을수록 평활한 그래프가 생성됩니다.
'''
df2 = df.assign(ewm_a_low=df['val'].ewm(alpha=0.1).mean()) #alpha=0.1로 df2 생성
df3 = df.assign(ewm_a_high=df['val'].ewm(alpha=0.7).mean()) #alpha=0.7로 df3 생성
ax = df.plot(kind='bar',x='index',y='val') 
ax2= df2.plot(kind='line',x='index', y='ewm_a_low', color='red', ax=ax) # alpha=0.1 은 적색
ax3= df3.plot(kind='line',x='index', y='ewm_a_high', color='green', ax=ax) # alpha=0.7 은 녹색
# plt.show()

'''
span 인수의 사용
span은 기간을 지정하여 평활계수를 계산하는 인수입니다. 계산식은 a = 2/(span+1)으로 계산 기간이 길어질수록 a가 작아집니다.
'''

df2 = df.assign(span_4=df['val'].ewm(span=4).mean())
df3 = df.assign(span_8=df['val'].ewm(span=8).mean())
ax = df.plot(kind='bar',x='index',y='val')
ax2= df2.plot(kind='line',x='index', y='span_4', color='red', ax=ax)
ax3= df3.plot(kind='line',x='index', y='span_8', color='green', ax=ax)
# plt.show()

'''
com 인수의 사용
com 은 질량중심 감쇠법으로 평활계수를 계산하는 인수입니다. 계산식은 a=1/(1+com)으로 com이 커질수록 a가 작아집니다.
'''
df2 = df.assign(com_2=df['val'].ewm(com=2).mean())
df3 = df.assign(com_10=df['val'].ewm(com=10).mean())
ax = df.plot(kind='bar',x='index',y='val')
ax2= df2.plot(kind='line',x='index', y='com_2', color='red', ax=ax)
ax3= df3.plot(kind='line',x='index', y='com_10', color='green', ax=ax)
# plt.show()


'''
halflife 인수의 사용
halflife인수는 반감기를 이용하여 평활계수를 계산하는 인수입니다. 계산식은 a=1-e^(-ln(2)/halflife) 으로 halflife가 길어질수록 a가 작아집니다.
'''
df2 = df.assign(harf_2=df['val'].ewm(halflife=2).mean())
df3 = df.assign(harf_5=df['val'].ewm(halflife=5).mean())
ax = df.plot(kind='bar',x='index',y='val')
ax2= df2.plot(kind='line',x='index', y='harf_2', color='red', ax=ax)
ax3= df3.plot(kind='line',x='index', y='harf_5', color='green', ax=ax)
# plt.show()

'''
adjust인수의 사용
상대적 가중치의 불균형을 해소하기위해 조정계수로 나눌지의 여부입니다. 대체로 값이 많을수록 adjust를 하는것이 유리합니다.
'''
df2 = df.assign(adj_True=df['val'].ewm(alpha=0.2,adjust=True).mean())
df3 = df.assign(adj_False=df['val'].ewm(alpha=0.2,adjust=False).mean())
ax = df.plot(kind='bar',x='index',y='val')
ax2= df2.plot(kind='line',x='index', y='adj_True', color='red', ax=ax)
ax3= df3.plot(kind='line',x='index', y='adj_False', color='green', ax=ax)
# plt.show()


'''
ignore_na인수의 사용
ignore_na는 결측치가 존재할 경우 가중치를 어떻게 설정할지 정하는 인수 입니다.

[x0, None, x1] 일때, 인 경우 ignore_na = False 이면 절대위치를 기반으로 하며,
x0와 x2의 가중치는 adjust = [ True인경우 (1-a)^2와 1 / False인 경우 (1-a)^2와 a ] 입니다.
[x0, None, x1] 일때, 인 경우 ignore_na = False 이면 절대위치를 기반으로 하며,
x0와 x2의 가중치는 adjust = [ True인경우 (1-a)와 1 / False인 경우 (1-a)와 a ] 입니다.
'''
df2 = df.assign(ignore_na_True=df['val'].ewm(alpha=0.2,ignore_na=True).mean())
df3 = df.assign(ignore_na_False=df['val'].ewm(alpha=0.2,ignore_na=False).mean())
ax = df.plot(kind='bar',x='index',y='val')
ax2= df2.plot(kind='line',x='index', y='ignore_na_True', color='red', ax=ax)
ax3= df3.plot(kind='line',x='index', y='ignore_na_False', color='green', ax=ax)
# plt.show()
