import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']  
plt.rcParams['axes.unicode_minus'] = False 

# 월별 이용정보
df_first = pd.read_csv('서울특별시 공공자전거 이용정보(1-6).csv', encoding="euc-kr")
df_second = pd.read_csv('서울특별시 공공자전거 이용정보(7-12).csv', encoding="euc-kr")
df_all = pd.concat([df_first, df_second], ignore_index = False)

df_code_month = df_all.groupby(['대여구분코드','대여일자'])['이용건수'].sum().unstack(0)
df_all['대여구분코드'] = df_all['대여구분코드'].replace({'일일권(비회원)': '일일권'})
df_code_month = df_all.groupby(['대여구분코드','대여일자'])['이용건수'].sum().unstack(0)

# 대여소별 이용정보
df = pd.read_csv('서울특별시 공공자전거 대여소별 이용정보(월별)_24.1-6.csv', encoding='cp949')
df1 = pd.read_csv('서울특별시 공공자전거 대여소별 이용정보(월별)_24.7-12.csv', encoding='cp949')
df_location = pd.concat([df, df1], ignore_index = False)
df_recovery = df_location.groupby('자치구')[['대여건수', '반납건수']].sum()
df_recovery['회수율'] = df_recovery['반납건수'] / df_recovery['대여건수'] * 100
df_recovery_sorted = df_recovery.sort_values(by='대여건수', ascending=False)

# 대여소별 그래프
fig, ax1 = plt.subplots(figsize=(14, 7))
x = np.arange(len(df_recovery_sorted.index))
width = 0.4

bar1 = ax1.bar(x - width/2, df_recovery_sorted['대여건수'],width=width, color='skyblue')
bar2 = ax1.bar(x + width/2, df_recovery_sorted['반납건수'],width=width, color='salmon')

ax2 = ax1.twinx()
line = ax2.plot(x, df_recovery_sorted['회수율'], color='green', marker='o', linewidth=2, label='회수율')

ax2.axhline(0, color='gray', linestyle='--', linewidth=1)
ax2.set_ylim(92, 108)
ax2.set_ylabel('회수율(%)', rotation=270, labelpad = 15)

ax1.set_ylabel('이용 건수 (단위 : 백만)')
ax1.set_title('서울특별시 공공자전거 대여소별 회수율', fontsize = 15, fontweight = 'bold', pad = 15)
ax1.set_xticks(x)
ax1.set_xticklabels(df_recovery_sorted.index, rotation=60)
ax1.legend()

lines_labels = [*zip([bar1, bar2], ['대여건수', '반납건수']), (line[0], '회수율')]
handles, labels = zip(*lines_labels)
ax1.legend(handles, labels, loc='upper right')
plt.tight_layout()
plt.show()
