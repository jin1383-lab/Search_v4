import streamlit as st
import time
from googleapiclient.discovery import build

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 다크모드 전용 CSS (컬러 테마: Dark + #dc3545 Red)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Shorts Finder",
    page_icon="🎬",
    layout="wide"
)

# 다크 테마 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 기본 글자색 (Dark Theme) */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* 사이드바 다크 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #2d2d2d;
    }
    
    /* 메인 버튼 및 포인트 컬러 (#dc3545) */
    .stButton>button {
        background-color: #dc3545;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #bb2d3b;
        color: #ffffff;
    }
    
    /* 프로그레스 바 컬러 */
    .stProgress > div > div > div > div {
        background-color: #dc3545;
    }
    
    /* 입력창 및 셀렉트박스 다크 스타일 */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #2b2b2b !important;
        color: #ffffff !important;
        border-color: #404040 !important;
    }

    /* 다크모드 카드 UI 스타일 */
    .card {
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 15px;
        background-color: #1e1e1e;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .card-title {
        color: #ffffff !important;
        text-decoration: none;
        font-weight: bold;
    }
    .card-title:hover {
        color: #dc3545 !important;
    }
    .card-info {
        color: #aaaaaa;
        font-size: 13px;
        margin-top: 6px;
    }

    /* 모바일 반응형 (max-width: 500px) */
    @media (max-width: 500px) {
        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. API 키 자동 로드 (Secrets 활용)
# -----------------------------------------------------------------------------
if "YOUTUBE_API_KEY" in st.secrets:
    api_key = st.secrets["YOUTUBE_API_KEY"]
    youtube = build("youtube", "v3", developerKey=api_key)
else:
    st.error("API 키가 설정되지 않았습니다. .streamlit/secrets.toml을 확인해주세요.")
    st.stop()

# -----------------------------------------------------------------------------
# 3. 사이드바 (데이터 관리 & API 사용량 & 홍보 링크)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("📁 데이터 관리")
    
    folder = st.selectbox("폴더 선택", ["기본 폴더", "엔터테인먼트", "지식/정보", "새 폴더 추가+"])
    
    st.divider()
    
    st.subheader("⚡ API 사용량")
    api_limit = 10000
    api_used = 2450  # 예시 사용량
    usage_pct = api_used / api_limit
    
    st.progress(usage_pct)
    st.caption(f"사용량: {api_used:,} / {api_limit:,} Quota ({int(usage_pct*100)}%)")
    
    st.divider()
    
    st.markdown("🔗 **추가 정보 및 커뮤니티**")
    st.markdown("[Dino High Class 커뮤니티 방문하기](https://cafe.naver.com/dinohighclass/349617)")

# -----------------------------------------------------------------------------
# 4. 메인 화면 (검색 및 데이터 디스플레이)
# -----------------------------------------------------------------------------
st.title("🎬 Shorts Finder")

# 검색 키워드
search_keywords = ["파이썬 기초", "유튜브 쇼츠 떡상", "Streamlit 사용법", "AI 영상 제작", "웹 크롤링"]
query = st.selectbox("🔍 검색어를 선택하거나 직접 입력하세요", options=[""] + search_keywords, index=0)

if not query:
    query = st.text_input("또는 직접 검색어 입력", placeholder="검색어를 입력하세요...")

search_btn = st.button("검색 실행")

# -----------------------------------------------------------------------------
# 5. 검색 결과 (다크모드 컴팩트 카드)
# -----------------------------------------------------------------------------
if search_btn or query:
    with st.spinner("데이터를 조회 중입니다..."):
        time.sleep(0.5)
    
    st.subheader(f"'{query}' 검색 결과")
    
    col1, col2 = st.columns(2)
    
    # 예시 카드 데이터
    dummy_data = [
        {"title": "쇼츠 조회수 100만 만드는 법칙", "channel": "채널 A", "views": "150만회", "url": "https://youtube.com", "thumb": "https://via.placeholder.com/300x170/2b2b2b/ffffff?text=Shorts+1"},
        {"title": "파이썬으로 웹앱 5분만에 만들기", "channel": "코딩 마스터", "views": "80만회", "url": "https://youtube.com", "thumb": "https://via.placeholder.com/300x170/2b2b2b/ffffff?text=Shorts+2"},
    ]
    
    for idx, item in enumerate(dummy_data):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.markdown(f"""
                <div class="card">
                    <img src="{item['thumb']}" style="width:100%; border-radius:6px; margin-bottom:10px;">
                    <a href="{item['url']}" target="_blank" class="card-title">{item['title']}</a>
                    <div class="card-info">
                        📺 <a href="{item['url']}" target="_blank" style="color:#aaa; text-decoration:none;">{item['channel']}</a> | 👁️ {item['views']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
