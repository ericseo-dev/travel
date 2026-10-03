import streamlit as st
from ai_helper import ask_ai
from user_manager import register_user, login_user, change_password, get_user_travels_file
from datetime import datetime
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="여행 기록문",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 배경 스타일 (흰색에서 하늘색으로 그라데이션)
st.markdown("""
    <style>
    body {
        background: linear-gradient(180deg, #ffffff 0%, #87ceeb 100%);
        min-height: 100vh;
    }
    .main {
        background: linear-gradient(180deg, #ffffff 0%, #87ceeb 100%);
    }
    .stApp {
        background: linear-gradient(180deg, #ffffff 0%, #87ceeb 100%);
    }
    .button-container {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin: 20px 0;
    }
    .ai-button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
    }
    .record-button {
        background-color: #2196F3;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
    }
    .plan-button {
        background-color: #f44336;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
    }
    .chat-message {
        padding: 12px;
        margin: 10px 0;
        border-radius: 8px;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .ai-message {
        background-color: #f5f5f5;
        text-align: left;
    }
    h1 {
        text-align: center;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

def load_travels(username=None):
    """저장된 여행 기록 불러오기"""
    if username:
        travels_file = f"{username}_travels.json"
    else:
        travels_file = "default_travels.json"

    if os.path.exists(travels_file):
        with open(travels_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_travels():
    """여행 기록 저장"""
    if st.session_state.logged_in and st.session_state.username:
        travels_file = f"{st.session_state.username}_travels.json"
    else:
        travels_file = "default_travels.json"

    with open(travels_file, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.travels, f, ensure_ascii=False, indent=2)

def get_latest_travel():
    """가장 최근 여행 정보 가져오기"""
    if st.session_state.travels:
        return st.session_state.travels[-1]
    return None

def ai_chat(user_message):
    """AI와 대화"""
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_message
    })

    # 대화 히스토리를 프롬프트에 포함
    conversation = "\n".join([
        f"{'사용자' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
        for msg in st.session_state.chat_history
    ])

    # AI 응답 생성
    ai_response = ask_ai(f"여행에 관한 친절한 여행 가이드로서 다음 대화를 계속해주세요:\n\n{conversation}")

    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': ai_response
    })

    return ai_response

def travel_planning_chat(user_message):
    """여행 계획 AI와 대화"""
    st.session_state.plan_messages.append({
        'role': 'user',
        'content': user_message
    })

    conversation = "\n".join([
        f"{'사용자' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
        for msg in st.session_state.plan_messages
    ])

    prompt = f"""당신은 전문 여행 계획자입니다. 사용자와 함께 멋진 여행 계획을 세우고 있습니다.
친절하고 자세하게 여행 계획을 도와주세요. 마지막 메시지가 "완료"이면 "여행 잘 갔다오세요!"라고 말하세요.

{conversation}"""

    ai_response = ask_ai(prompt)

    st.session_state.plan_messages.append({
        'role': 'assistant',
        'content': ai_response
    })

    return ai_response

# 로그인 페이지
def login_page():
    st.title("✈️ 여행 기록문")
    st.markdown("---")
    st.markdown("### 🔐 로그인")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("사용자명", placeholder="사용자명을 입력하세요")
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")

        col_login, col_signup = st.columns(2)

        with col_login:
            if st.button("로그인", use_container_width=True):
                if username and password:
                    success, message = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.travels = load_travels(username)
                        st.session_state.page = 'home'
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("⚠️ 사용자명과 비밀번호를 입력해주세요!")

        with col_signup:
            if st.button("회원가입", use_container_width=True):
                st.session_state.page = 'signup'
                st.rerun()

# 회원가입 페이지
def signup_page():
    st.title("✈️ 여행 기록문")
    st.markdown("---")
    st.markdown("### 📝 회원가입")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        new_username = st.text_input("사용자명", placeholder="3글자 이상 입력하세요")
        new_password = st.text_input("비밀번호", type="password", placeholder="4글자 이상 입력하세요")
        new_password_confirm = st.text_input("비밀번호 확인", type="password", placeholder="비밀번호를 다시 입력하세요")

        if st.button("가입하기", use_container_width=True):
            if new_username and new_password and new_password_confirm:
                if new_password != new_password_confirm:
                    st.error("⚠️ 비밀번호가 일치하지 않습니다!")
                else:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message)
                        st.info("로그인 페이지에서 로그인 해주세요!")
                        st.session_state.page = 'login'
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("⚠️ 모든 필드를 입력해주세요!")

        st.markdown("---")
        if st.button("← 로그인으로 돌아가기", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

# 홈 페이지
def home_page():
    st.title("✈️ 여행 기록문")

    # 사용자 정보 표시
    col_user, col_logout, col_pwd = st.columns([2, 1, 1])

    with col_user:
        st.write(f"👤 **{st.session_state.username}** 님 환영합니다!")

    with col_pwd:
        if st.button("🔑 비밀번호 변경", use_container_width=True):
            st.session_state.page = 'change_password'
            st.rerun()

    with col_logout:
        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.page = 'login'
            st.session_state.travels = []
            st.rerun()

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 AI와 대화", key="ai_btn", use_container_width=True):
            st.session_state.page = 'ai_chat'
            st.rerun()

    with col2:
        if st.button("📝 여행 기록", key="record_btn", use_container_width=True):
            st.session_state.page = 'record_travel'
            st.rerun()

    with col3:
        if st.button("🗺️ 여행 계획", key="plan_btn", use_container_width=True):
            st.session_state.page = 'plan_travel'
            st.rerun()

    st.markdown("---")
    st.markdown("### 🌍 최근 여행 기록")

    if st.session_state.travels:
        for i, travel in enumerate(reversed(st.session_state.travels)):
            with st.container():
                st.write(f"**📍 {travel.get('location', '장소 미기입')}**")
                st.write(f"📅 {travel.get('date', '날짜 미기입')}")
                st.write(f"✨ {travel.get('highlights', '기록 미기입')}")
                st.divider()
    else:
        st.info("아직 여행 기록이 없습니다. 여행 기록 버튼을 눌러서 시작해보세요!")

# AI 대화 페이지
def ai_chat_page():
    st.title("🤖 AI와의 여행 대화")

    if st.button("← 돌아가기", key="back_ai"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown("---")

    # AI 인사말
    if not st.session_state.ai_greeted and len(st.session_state.chat_history) == 0:
        greeting = "안녕하세요! 저는 여행 가이드입니다. 여행에 대해 궁금한 점이 있으시면 편하게 물어봐주세요! 😊"
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': greeting
        })
        st.session_state.ai_greeted = True

    # 대화 히스토리 표시
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.write(f"**당신:** {message['content']}")
        else:
            st.write(f"**AI:** {message['content']}")
        st.markdown("---")

    # 사용자 입력
    user_input = st.text_input("여행에 대해 물어보세요:", key="ai_input")

    if user_input:
        with st.spinner("AI가 생각 중입니다..."):
            response = ai_chat(user_input)
            st.rerun()

# 비밀번호 변경 페이지
def change_password_page():
    st.title("✈️ 여행 기록문")
    st.markdown("---")
    st.markdown("### 🔑 비밀번호 변경")

    if st.button("← 돌아가기", key="back_pwd"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        old_password = st.text_input("기존 비밀번호", type="password", placeholder="기존 비밀번호를 입력하세요")
        new_password = st.text_input("새 비밀번호", type="password", placeholder="새 비밀번호를 입력하세요 (4글자 이상)")
        new_password_confirm = st.text_input("새 비밀번호 확인", type="password", placeholder="새 비밀번호를 다시 입력하세요")

        if st.button("비밀번호 변경", use_container_width=True):
            if old_password and new_password and new_password_confirm:
                if new_password != new_password_confirm:
                    st.error("⚠️ 새 비밀번호가 일치하지 않습니다!")
                else:
                    success, message = change_password(
                        st.session_state.username,
                        old_password,
                        new_password
                    )
                    if success:
                        st.success(message)
                        st.session_state.page = 'home'
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("⚠️ 모든 필드를 입력해주세요!")

# 여행 기록 페이지
def record_travel_page():
    st.title("📝 여행 기록하기")

    if st.button("← 돌아가기", key="back_record"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown("---")

    with st.form("travel_form"):
        location = st.text_input("📍 어디에 다녀왔나요?", placeholder="예: 서울, 부산, 일본 도쿄")
        date = st.date_input("📅 언제 다녀왔나요?")
        highlights = st.text_area("✨ 여행에서 좋았던 점들:", placeholder="예: 맛있는 음식, 아름다운 경치, 새로운 친구들...")

        submitted = st.form_submit_button("기록 저장", use_container_width=True)

        if submitted:
            if location and highlights:
                travel_record = {
                    'location': location,
                    'date': str(date),
                    'highlights': highlights,
                    'saved_at': datetime.now().isoformat()
                }
                st.session_state.travels.append(travel_record)
                save_travels()
                st.success("✅ 여행 기록이 저장되었습니다!")
                st.balloons()
                st.session_state.page = 'home'
                st.rerun()
            else:
                st.error("⚠️ 모든 필드를 입력해주세요!")

# 여행 계획 페이지
def plan_travel_page():
    st.title("🗺️ AI와 함께 여행 계획하기")

    if st.button("← 돌아가기", key="back_plan"):
        st.session_state.page = 'home'
        st.session_state.plan_messages = []
        st.rerun()

    st.markdown("---")

    # 대화 히스토리 표시
    for message in st.session_state.plan_messages:
        if message['role'] == 'user':
            st.write(f"**당신:** {message['content']}")
        else:
            st.write(f"**AI:** {message['content']}")
        st.markdown("---")

    # 첫 메시지 자동 생성
    if len(st.session_state.plan_messages) == 0:
        initial_prompt = "사용자가 여행 계획을 시작했습니다. 친절하게 인사하고 어떤 여행을 계획하고 싶은지 물어봐주세요."
        initial_message = ask_ai(initial_prompt)
        st.session_state.plan_messages.append({
            'role': 'assistant',
            'content': initial_message
        })
        st.rerun()

    # 사용자 입력
    user_input = st.text_input("여행 계획을 알려주세요:", placeholder="예: 5일간 유럽 여행을 계획하고 싶어요", key="plan_input")

    col1, col2 = st.columns([3, 1])

    with col1:
        if user_input:
            with st.spinner("AI가 계획을 짜고 있습니다..."):
                response = travel_planning_chat(user_input)
                st.rerun()

    with col2:
        if st.button("✅ 완료", use_container_width=True):
            with st.spinner("최종 인사말을 준비 중입니다..."):
                final_message = travel_planning_chat("완료")
                st.rerun()

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = 'login' if not st.session_state.logged_in else 'home'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'ai_greeted' not in st.session_state:
    st.session_state.ai_greeted = False
if 'travels' not in st.session_state:
    st.session_state.travels = load_travels() if st.session_state.logged_in else []
if 'planning_mode' not in st.session_state:
    st.session_state.planning_mode = False
if 'plan_messages' not in st.session_state:
    st.session_state.plan_messages = []

# 로그인하지 않으면 로그인 페이지로
if not st.session_state.logged_in:
    if st.session_state.page == 'signup':
        signup_page()
    else:
        login_page()
# 페이지 라우팅
elif st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'ai_chat':
    ai_chat_page()
elif st.session_state.page == 'record_travel':
    record_travel_page()
elif st.session_state.page == 'plan_travel':
    plan_travel_page()
elif st.session_state.page == 'change_password':
    change_password_page()
