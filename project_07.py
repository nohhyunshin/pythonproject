import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt 

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']  
plt.rcParams['axes.unicode_minus'] = False 

df_3years = pd.read_csv('서울특별시_공공자전거_이용정보(월별)_22-24.csv', encoding='cp949')

monthly_total = df_3years.groupby('대여일자')['이용건수'].sum()
monthly_total.index = pd.to_datetime(monthly_total.index, format='%Y%m')
monthly_total = monthly_total.sort_index()

# 이동 평균 계산 (3개월, 6개월)
df_monthly = pd.DataFrame({'이용건수': monthly_total})
df_monthly['MA_3'] = df_monthly['이용건수'].rolling(window=3).mean()
df_monthly['MA_6'] = df_monthly['이용건수'].rolling(window=6).mean()

# 시각화
plt.figure(figsize=(12, 6))

plt.plot(df_monthly.index, df_monthly['이용건수'], color='skyblue', label='이용건수', linewidth=2)
plt.fill_between(df_monthly.index, df_monthly['이용건수'], color='skyblue', alpha = 0.2)

plt.plot(df_monthly['MA_3'], label='3개월 이동 평균', color='orange', linewidth=3)
plt.plot(df_monthly['MA_6'], label='6개월 이동 평균', color='green', linewidth=3)

plt.title('서울특별시 공공자전거 이동 평균', fontsize = 15, fontweight = 'bold', pad = 15)
plt.ylabel('이용 건수 (단위 : 백만)')
plt.ylim(bottom=0)      # y축이 0에서 시작하게

plt.legend()
plt.grid(True, alpha = 0.2)

plt.tight_layout()
plt.show()