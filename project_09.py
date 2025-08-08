import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt 

# 선형 회귀 분석
plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']  
plt.rcParams['axes.unicode_minus'] = False 

df_3years = pd.read_csv('서울특별시_공공자전거_이용정보(월별)_22-24.csv', encoding='cp949')

monthly_total = df_3years.groupby('대여일자')['이용건수'].sum()
monthly_total.index = pd.to_datetime(monthly_total.index, format='%Y%m')
monthly_total = monthly_total.sort_index()

df_monthly = pd.DataFrame({'이용건수': monthly_total})

df_monthly['월번호'] = np.arange(len(df_monthly))
x = df_monthly['월번호']
y = df_monthly['이용건수']

# 1차 다항 회귀 (선형 회귀)
a, b  = np.polyfit(x, y, deg=1)     # x와 y 데이터를 1차 방정식의 계수를 계산

# 미래 6개월 예측
future_x = np.arange(len(x) + 6) 
future_y = a * future_x + b

# 날짜 인덱스 생성 (예측 포함)
future_dates = pd.date_range(
    start=df_monthly.index.min(),
    periods=len(future_x),
    freq='MS'                   # month start (매달 시작일)
)

# 미래 예측 시각화
plt.figure(figsize=(12, 6))
plt.plot(df_monthly.index, y, label='이용 건수', color='skyblue')
plt.fill_between(df_monthly.index, df_monthly['이용건수'], color='skyblue', alpha=0.2)

plt.plot(future_dates, future_y, label='선형 추세선 (예측 포함)', color='red', linestyle='--', linewidth=3)

plt.title('서울특별시 공공자전거 수요 예측', fontsize = 15, fontweight = 'bold', pad = 15)
plt.ylabel('이용 건수 (단위 : 백만)')
plt.ylim(bottom = 0)

plt.legend()
plt.grid(True, alpha = 0.2)

plt.tight_layout()
plt.show()