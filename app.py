import streamlit as st
import google.generativeai as genai

# Gemini API 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 페이지 설정
st.set_page_config(page_title="Gemini 챗봇", page_icon="💬")

# 제목과 설명
st.title("💬 Gemini 기반 챗봇")
st.caption("Gemini 1.5 Flash 기반 기본 챗봇 프레임워크")

# 세션 상태 초기화 (채팅 기록)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 이전 입력값 초기화를 위한 세션 상태
if "is_processed" not in st.session_state:
    st.session_state.is_processed = False

# 입력 콜백 함수
def submit():
    if st.session_state.user_input and not st.session_state.is_processed:
        # 현재 입력값 저장
        current_input = st.session_state.user_input
        
        # 처리 상태 표시
        st.session_state.is_processed = True
        
        # 사용자 메시지를 채팅 기록에 추가
        st.session_state.chat_history.append({
            "role": "user",
            "parts": [current_input]
        })
        
        # Gemini API를 통해 응답 생성
        messages = [{"role": m["role"], "parts": m["parts"]} for m in st.session_state.chat_history]
        response = model.generate_content(messages)
        
        # 챗봇 응답을 채팅 기록에 추가
        st.session_state.chat_history.append({
            "role": "model",
            "parts": [response.text]
        })
        
        # 입력창 초기화
        st.session_state.user_input = ""

# 채팅 기록 표시
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**👤 사용자:** {message['parts'][0]}")
    else:
        st.markdown(f"**🤖 챗봇:** {message['parts'][0]}")

# 사용자 입력
st.text_input(
    "질문을 입력하세요:",
    key="user_input",
    on_change=submit
)

# 새로운 입력을 받을 준비
if not st.session_state.user_input:
    st.session_state.is_processed = False
