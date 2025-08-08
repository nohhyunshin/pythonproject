import os
import customtkinter as ctk
from project_06 import show_outliers

# CTk 클래스 생성으로 window 창 생성
window = ctk.CTk()

# Tkinter 테마 설정
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('dark-blue')

# window 창의 크기 및 초기 위치 설정
window_width = 600
window_height = 500
screen_width = window.winfo_screenwidth()          # 기기별 넓이
screen_height = window.winfo_screenheight()        # 기기별 높이

# window 창의 위치를 사용자 기기의 정중앙이 되도록
window_pos_x = (screen_width // 2) - (window_width // 2)
window_pos_y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{window_pos_x}+{window_pos_y}")

# window 창 크기 자동 조절 가능 여부
window.resizable(False, False)          # 불가능

# window 창 이름
window.title("서울특별시 공공자전거 이용 정보")

# window 창 내 라벨 설정
label = ctk.CTkLabel(window, text = "어떤 정보를 확인하시겠습니까?",
                     font = ('HYGothic-Medium', 30, 'bold'))
label.pack(pady = 30)

# 버튼별 동작 할당
def monthly_seasonal() : os.system('python project01/project_01.py')            # 월별 일일권 / 정기권 이용 건수
def monthly_ages() : os.system('python project01/project_02.py')                # 연령대별 이용 건수
def monthly_ages_users() : os.system('python project01/project_03.py')          # 월별 연령대별 이용 비율
def monthly_users() : os.system('python project01/project_04.py')               # 월별 이용 건수
def region_rental() : os.system('python project01/project_05.py')               # 자치구별 수요 분석
def outlines() : show_outliers()                                                # 이상치 탐지 테이블
def moving_average() : os.system('python project01/project_07.py')              # 이동 평균선
def timelines() : os.system('python project01/project_08.py')                   # 시계열 데이터
def future() : os.system('python project01/project_09.py')                      # 선형 회귀 (미래 예측)
def exit_window() : window.destroy()        # window 닫기 버튼

# 버튼 배치용 프레임 생성
button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=20)

# 버튼 목록
buttons = [
    ("일일권 / 정기권 이용 건수", monthly_seasonal),
    ("연령대별 이용 건수", monthly_ages),
    ("연령대별 이용 비율 (월별)", monthly_ages_users),
    ("월별 이용 건수", monthly_users),
    ("자치구별 수요 분석", region_rental),
    ("이상치 분석", outlines),
    ("이동 평균선", moving_average),
    ("시계열 데이터", timelines),
    ("미래 예측 (선형 회귀)", future),
    ("종료", exit_window)
]

# 버튼들을 2열로 배치
for index, (text, command) in enumerate(buttons):
    row = index // 2
    col = index % 2
    button = ctk.CTkButton(button_frame, text=text, command=command, corner_radius=5,
                           width=260, height=50, font=('Malgun Gothic', 18))
    button.grid(row=row, column=col, padx=12, pady=12)

window.mainloop()