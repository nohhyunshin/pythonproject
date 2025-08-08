import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt 

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']  
plt.rcParams['axes.unicode_minus'] = False 

df_3years = pd.read_csv('서울특별시_공공자전거_이용정보(월별)_22-24.csv', encoding='cp949')

monthly_total = df_3years.groupby('대여일자')['이용건수'].sum()
monthly_total.index = pd.to_datetime(monthly_total.index, format='%Y%m')
monthly_total = monthly_total.sort_index()

# 시계열 데이터
result = seasonal_decompose(monthly_total, model='additive', period=12)
fig = result.plot()
fig.set_size_inches(10, 6)

plt.tight_layout()
plt.show()