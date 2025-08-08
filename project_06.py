import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df_first = pd.read_csv('서울특별시 공공자전거 이용정보(1-6).csv', encoding="euc-kr")
df_second = pd.read_csv('서울특별시 공공자전거 이용정보(7-12).csv', encoding="euc-kr")

# 데이터 병합
df_all = pd.concat([df_first, df_second], ignore_index = False)

# 대여일자 컬럼을 datetime 형식으로 변환 > 월만 추출
df_all['대여월'] = pd.to_datetime(df_all['대여일자'], format = "%Y%m").dt.month

# 월별 이용 건수
monthly_users_total = df_all.groupby('대여월')['이용건수'].sum()
monthly_users = df_all.groupby('대여월')['이용건수'].sum().reset_index()

# 전월 대비 증감률(%) 계산
monthly_users['전월대비증감률'] = monthly_users['이용건수'].pct_change() * 100

# 이상치 탐지: 증감률이 ±10% 이상인 경우
outliers = monthly_users[monthly_users['전월대비증감률'].abs() >= 10]

def show_table(df):
    window = tk.Toplevel()
    window.geometry("500x220")
    window.title("이상치 분석")

    style = ttk.Style()
    style.configure("Treeview", font=("Malgun Gothic", 13), rowheight=30)
    style.configure("Treeview.Heading", font=("Malgun Gothic", 13, "bold"))

    tree = ttk.Treeview(window, columns=list(df.columns), show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor=tk.CENTER)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

def show_outliers():
    df = outliers.copy()
    df['대여월'] = df['대여월'].apply(lambda x: f"{x}월")
    df['이용건수'] = df['이용건수'].apply(lambda x: f"{int(x):,}건")
    df['전월대비증감률'] = df['전월대비증감률'].apply(lambda x: f"{x:.2f}%")
    
    show_table(df[['대여월', '이용건수', '전월대비증감률']])

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 메인 루트 창 숨김
    show_outliers()
    root.mainloop()