import tkinter as tk
from tkinter import ttk
import pandas as pd
import datetime

# 엑셀의 시간(소수점)을 우리가 아는 시간(HH:MM)으로 바꿔주는 함수
def format_excel_time(val):
    # 1. 이미 "09:30" 같은 문자열인 경우
    if isinstance(val, str):
        return val
    # 2. 파이썬 내부 시간 객체로 읽힌 경우
    elif isinstance(val, datetime.time):
        return val.strftime("%H:%M")
    # 3. 엑셀의 소수점으로 읽힌 경우 (하루=1로 계산)
    elif isinstance(val, float) and pd.notna(val):
        total_minutes = int(round(val * 24 * 60))
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
    
    return str(val) if pd.notna(val) else ""

def load_routine():
    try:
        # skiprows=4로 설정하여 표의 실제 데이터부터 읽어옵니다.
        df = pd.read_excel('daily_routine_plan.xlsx', sheet_name='루틴 체크표', skiprows=4)
        return df
    except Exception as e:
        print(f"엑셀 파일을 읽는 중 오류 발생: {e}")
        return None

def create_gui():
    window = tk.Tk()
    window.title("평일 완벽 루틴 관리기")
    window.geometry("600x450")

    weekday_idx = datetime.datetime.today().weekday()

    # 요일별 맞춤 멘트 설정
    messages = {
        0: " 반팔 꽉끼는 삼두로 만드는 거야. (가슴, 삼두)",
        1: " 팔 운동으로 죽는 느낌 and 등에 미친 새끼",
        2: " 하체 재활 훈련에 들어간 미친놈",
        3: " 어깨를 만들기 위한 상급 노하우",
        4: " 상체 죽이기",
        5: " 익-스",
        6: " 익-스"
    }

    # 오늘 요일에 맞는 멘트를 가져옴
    today_msg = messages.get(weekday_idx, "오늘도 활기차게 루틴을 시작해볼까요?")
    
    # 상단 타이틀에 요일별 멘트 적용
    lbl_title = tk.Label(window, text=today_msg, font=("맑은 고딕", 14, "bold"))
    lbl_title.pack(pady=20)

    tree = ttk.Treeview(window, columns=("time", "task", "status"), show="headings")
    tree.heading("time", text="시간 (기준)")
    tree.heading("task", text="일정")
    tree.heading("status", text="달성 여부")

    tree.column("time", width=120, anchor="center")
    tree.column("task", width=300, anchor="w")
    tree.column("status", width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    df = load_routine()
    if df is not None:
        for index, row in df.iterrows():
            raw_time = row.get('시간 (기준)')
            task_val = row.get('일정')
            
            # 값이 둘 다 존재할 때만 표에 삽입
            if pd.notna(raw_time) and pd.notna(task_val):
                # 방금 만든 시간 변환 함수를 적용
                time_val = format_excel_time(raw_time)
                tree.insert("", "end", values=(time_val, task_val, "[ ]"))

    window.mainloop()

if __name__ == "__main__":
    create_gui()