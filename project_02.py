import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

# y축 포맷 설정 함수 (만 단위)
def millions_formatter(x, pos):
    return f'{int(x/10_000)}'  # 만 단위로 나눠서 M 표기

# 데이터 불러오기
df_first = pd.read_csv('서울특별시 공공자전거 이용정보(1-6).csv', encoding="euc-kr")
df_second = pd.read_csv('서울특별시 공공자전거 이용정보(7-12).csv', encoding="euc-kr")

# 데이터 병합
df_all = pd.concat([df_first, df_second], ignore_index = False)

# 대여일자 컬럼을 datetime 형식으로 변환 > 월만 추출
df_all['대여월'] = pd.to_datetime(df_all['대여일자'], format = "%Y%m").dt.month

# 연령대별 이용 건수
# 연령대 코드를 원하는 순서로 정렬
age_order = ['~10대','20대', '30대', '40대', '50대', '60대', '70대이상', '기타']
df_all['연령대코드'] = pd.Categorical(df_all['연령대코드'], categories = age_order, ordered = True)
ages = df_all.groupby('연령대코드', observed=False).size().sort_index()

# 시각화
plt.figure(figsize = (10, 6))
bar_spacing = 0.4

plt.bar(ages.index, ages.values, width = bar_spacing, color = "#5685EC")
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))      # y축 단위 조정

# 데이터 레이블
for idx, val in enumerate(ages):
    plt.text(idx, val, f"{round(val / 10_000)}만", ha='center', va='bottom')

plt.title('서울특별시 공공자전거 이용 건수 (연령대별)', fontsize = 15, fontweight = 'bold', pad = 15)
plt.ylabel('이용 건수 (단위 : 만)')

plt.tight_layout()
plt.show()