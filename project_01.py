# 일일권 / 정기권 이용 건수 시각화
# 월별 총 이용 건수 시각화
# 막대 그래프와 표식 있는 꺾은 선 그래프로 복합 출력

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df_first = pd.read_csv('서울특별시 공공자전거 이용정보(1-6).csv', encoding="euc-kr")
df_second = pd.read_csv('서울특별시 공공자전거 이용정보(7-12).csv', encoding="euc-kr")

# 데이터 병합
df_all = pd.concat([df_first, df_second], ignore_index = False)

# 일일권 / 정기권 이용 건수
daily_ticket = (df_all['대여구분코드'] == '일일권').sum()
season_ticket = (df_all['대여구분코드'] == '정기권').sum()
all_users = daily_ticket + season_ticket    # 총 이용 건수

# 대여일자 컬럼을 datetime 형식으로 변환 > 월만 추출
df_all['대여월'] = pd.to_datetime(df_all['대여일자'], format = "%Y%m").dt.month

# 월별 일일권 / 정기권 이용 건수
daily_ticket_users = df_all[df_all['대여구분코드']=='일일권'].groupby('대여월')
season_ticket_users = df_all[df_all['대여구분코드']=='정기권'].groupby('대여월')
daily_ticket_sum = daily_ticket_users['이용건수'].sum()
season_ticket_sum = season_ticket_users['이용건수'].sum()

# 탄소 저감률
carbon_reducation_daily = daily_ticket_users['탄소량'].sum()
carbon_reducation_season = season_ticket_users['탄소량'].sum()

# 시각화
plt.figure(figsize = (15, 8))
bar_spacing = 0.4       # 막대 그래프 사이 간격 조정

# 월별 일일권 이용 건수
plt.bar(daily_ticket_sum.index - bar_spacing/2, daily_ticket_sum.values,
         color = "#3cb371", label = '일일권', width = bar_spacing)

# 데이터 레이블
for idx, val in zip(daily_ticket_sum.index - bar_spacing/2, daily_ticket_sum.values):
    plt.text(idx, val+50, f"{round(val / 1_000_000, 1)}M", ha='center', va='bottom', fontweight = '500', fontsize = 11)

# 월별 정기권 이용 건수
plt.bar(season_ticket_sum.index + bar_spacing/2, season_ticket_sum.values,
         color = "#3c5cb3", label = '정기권', width = bar_spacing)

# 데이터 레이블
for idx, val in zip(season_ticket_sum.index + bar_spacing/2, season_ticket_sum.values):
    plt.text(idx, val+50, f"{round(val / 1_000_000, 1)}M", ha='center', va='bottom', fontweight = '500', fontsize = 11)

plt.plot(carbon_reducation_daily.index, carbon_reducation_daily.values, linewidth = 2,
         label = '일일권 탄소 저감량(Kg)', marker = 'o', color = "#FFCB59")
plt.plot(carbon_reducation_season.index, carbon_reducation_season.values, linewidth = 2,
         label = '정기권 탄소 저감량(Kg)', marker = 'o', color = "#FF5F54")

plt.title("서울특별시 공공자전거 사용 유형별 이용 건수", fontsize = 15, fontweight = 'bold', pad = 15)
plt.xticks(ticks=range(1, 13))
plt.xlim(0.5, 12.5)
plt.ylabel("이용 건수 (단위 : 백만)")
plt.legend()
plt.grid(True, alpha = 0.2)

plt.tight_layout()
plt.show()