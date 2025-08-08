# 월별 이용 건수

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df_first = pd.read_csv('서울특별시 공공자전거 이용정보(1-6).csv', encoding="euc-kr")
df_second = pd.read_csv('서울특별시 공공자전거 이용정보(7-12).csv', encoding="euc-kr")
df_weather = pd.read_csv('서울 기온 정보_2024.csv', encoding = 'euc-kr')
# print(df_weather)

# 데이터 병합
df_all = pd.concat([df_first, df_second], ignore_index = False)

# 대여일자 컬럼을 datetime 형식으로 변환 > 월만 추출
df_all['대여월'] = pd.to_datetime(df_all['대여일자'], format = "%Y%m").dt.month

# 월별 연령대별 이용 건수 (최대)
monthly_age_max = df_all.groupby(['대여월', '연령대코드'])['이용건수'].max()
print(f"월별 연령대별 최대 이용 건수 : {monthly_age_max}")

# 월별 이용 건수
monthly_users_total = df_all.groupby('대여월')['이용건수'].sum()
monthly_users = df_all.groupby('대여월')['이용건수'].sum().reset_index()
print(f"월별 이용 건수 : {monthly_users_total.to_dict()}")

# 월별 최대 이용 건수
monthly_users_max = df_all.groupby('대여월')['이용건수'].max()
print(f"월별 최대 이용 건수 : {monthly_users_max.to_dict()}")

# 서울 기온 정보_2024 파일에서 일시(월) 추출
df_weather['일시'] = pd.to_datetime(df_weather['일시'])
df_weather['일시월'] = df_weather['일시'].dt.month

# 평균 기온 및 강수량
weather = df_weather.groupby('일시월')['강수량']
celsius = df_weather.groupby('일시월')['평균기온']

# 시각화
fig, ax1 = plt.subplots(figsize=(10, 6))

plt.bar(monthly_users_total.index, monthly_users_total.values, width = 0.6, color = "#EBAE46")
plt.title('서울특별시 공공자전거 이용 건수 (월별)', fontsize = 15, fontweight = 'bold', pad = 15)
plt.ylabel('이용 건수 (단위 : 백만)')

# 데이터 레이블
for x, val in zip(monthly_users_total.index, monthly_users_total.values):
     plt.text(x, val + 50, f"{round(val / 1_000_000, 1)}M", ha='center', va='top', rotation = 90)

# 강수량과 평균 기온 시각화
ax1.twinx()        # 보조축
rain_cm = df_weather['강수량'] / 10

plt.plot(df_weather['일시월'], df_weather['평균기온'], linewidth = 2,
         color="#CF0F47", marker='o', label='평균기온(℃)')

plt.plot(df_weather['일시월'], rain_cm, linewidth = 2,
         color='#5EABD6', marker='o', label='강수량(cm)')

plt.legend()
plt.tight_layout()
plt.show()