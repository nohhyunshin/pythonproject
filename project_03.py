# 월별 연령대별 이용 건수

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

# y축 포맷 설정 함수 (만 단위)
def millions_formatter(x, pos):
    return f'{int(x/1_000)}K'  # 천 단위로 나눠서 M 표기

# 데이터 불러오기
df_first = pd.read_csv('서울특별시 공공자전거 이용정보(1-6).csv', encoding="euc-kr")
df_second = pd.read_csv('서울특별시 공공자전거 이용정보(7-12).csv', encoding="euc-kr")

# 데이터 병합
df_all = pd.concat([df_first, df_second], ignore_index = False)

# 대여일자 컬럼을 datetime 형식으로 변환 > 월만 추출
df_all['대여월'] = pd.to_datetime(df_all['대여일자'], format = "%Y%m").dt.month

# 월별 연령대별 이용 건수
monthly_age_users = df_all.groupby(['대여월', '연령대코드'])['이용건수'].size().unstack()

# 시각화
bar_spacing = 0.4
colors = ["#FFF9BD", "#DEE791", "#FFD6BA", "#CAE8BD",  '#9ECAD6', "#67AE6E", "#FED16A", "#328E6E"]
ax = monthly_age_users.plot(kind='bar', figsize=(15,8), color = colors[:len(monthly_age_users.columns)], width = bar_spacing*2, rot=0)
ax.set_xlabel("")
ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))      # y축 단위 조정

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=8, frameon=False)

# 라벨 설정
plt.title('서울특별시 공공자전거 이용 건수 (연령별, 월별)', fontsize = 15, fontweight = 'bold', pad = 15)
plt.ylabel('이용 건수 (단위 : 천)')

plt.tight_layout()
plt.show()