import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


df2 = pd.read_csv('/Users/dymacpro/myProject/myDev/My/goorm-ai-study/260127_Pandas_/kaggle/input/goldstock v1.csv')

fig = px.line(
  data_frame= df2,
  x = 'Date',
  y = ['Open', 'Close'],
  color_discrete_sequence=['#b8473e', '#329dba'],
  title= 'Gold Open & Close Price'
)

fig.show()