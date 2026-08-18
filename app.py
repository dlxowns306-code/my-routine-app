import streamlit as st
import pandas as pd
import datetime

# 1. 페이지 기본 설정 (스마트폰 화면에 맞게 꽉 차게 설정)
st.set_page_config(page_title="평일 완벽 루틴 관리기", page_icon="🔥", layout="centered")

# 2. 엑셀 시간 변환 함수 (기존과 동일)
def format_excel_time(val):
    if isinstance(val, str):
        return val
    elif isinstance(val, datetime.time):
        return val.strftime("%H:%M")
    elif isinstance(val, float) and pd.notna(val):
        total_minutes = int(round(val * 24 * 60))
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
    return str(val) if pd.notna(val) else ""

# 3. 데이터 불러오기
# @st.cache_data를 붙이면 폰에서 접속할 때마다 엑셀을 다시 읽지 않아 속도가 훨씬 빠릅니다.
@st.cache_data
def load_routine():
    try:
        df = pd.read_excel('daily_routine_plan.xlsx', sheet_name='루틴 체크표', skiprows=4)
        
        # 새로운 표를 깔끔하게 만들기
        clean_df = pd.DataFrame()
        clean_df['시간 (기준)'] = df.iloc[:, 1].apply(format_excel_time)
        clean_df['일정'] = df.iloc[:, 2]
        
        # 빈 줄과 제목 줄 제거
        clean_df = clean_df.dropna()
        clean_df = clean_df[clean_df['일정'] != '']
        clean_df = clean_df[~clean_df['시간 (기준)'].str.contains('시간', na=False)]
        
        # ⭐ 모바일 터치용 실제 체크박스 열 추가 (기본값은 False = 빈 칸)
        clean_df['달성 완료'] = False
        
        return clean_df
    except Exception as e:
        st.error(f"엑셀 파일을 읽는 중 오류 발생: {e}")
        return None

# 4. 메인 화면 구성
def main():
    # 요일별 맞춤 멘트
    weekday_idx = datetime.datetime.today().weekday()
    messages = {
        0: " 반팔 꽉끼는 삼두로 만드는 거야. (가슴, 삼두)",
        1: " 팔 운동으로 죽는 느낌 and 등에 미친 새끼",
        2: " 하체 재활 훈련에 들어간 미친놈",
        3: " 어깨를 만들기 위한 상급 노하우",
        4: " 상체 죽이기",
        5: " 익-스",
        6: " 익-스"
    }
    today_msg = messages.get(weekday_idx, "오늘도 죽는느낌")

    # 화면에 그리기
    st.title("📝 나만의 루틴 관리기")
    st.subheader(today_msg)
    st.write("---")

    df = load_routine()

    if df is not None and not df.empty:
        # st.data_editor를 쓰면 표 안에 실제 터치 가능한 체크박스가 생깁니다!
        edited_df = st.data_editor(
            df,
            column_config={
                "달성 완료": st.column_config.CheckboxColumn(
                    "달성 완료 ✅",
                    help="루틴을 완료했으면 터치해서 체크하세요!",
                    default=False,
                )
            },
            disabled=["시간 (기준)", "일정"], # 시간과 일정은 실수로 터치해도 수정 안 되게 잠금
            hide_index=True,
            use_container_width=True
        )
        
        # 보너스 기능: 진행률 게이지 바 (몇 퍼센트 달성했는지 보여줌)
        total_tasks = len(edited_df)
        completed_tasks = edited_df['달성 완료'].sum()
        progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
        
        st.write("---")
        st.subheader(f"🏃 오늘의 진행률: {progress}% ({completed_tasks}/{total_tasks})")
        st.progress(progress / 100)

if __name__ == "__main__":
    main()