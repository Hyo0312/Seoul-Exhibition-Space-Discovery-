import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Seoul Space Discovery",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.main { background-color: #faf7f2; }
[data-testid="stSidebar"] {
    background-color: #f4efe6;
    border-right: 1px solid #ddd5c8;
}
[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* Metric cards */
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #ddd5c8;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 12px rgba(80,55,35,.07);
}
div[data-testid="metric-container"] label {
    color: #a8998a !important;
    font-size: 11px !important;
    letter-spacing: .12em;
    text-transform: uppercase;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #c4714a !important;
    font-size: 2rem !important;
}

/* Place cards */
.place-card {
    background: #ffffff;
    border: 1.5px solid #ddd5c8;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(80,55,35,.07);
    transition: border-color .2s;
}
.place-card:hover { border-color: #c4714a; }
.card-title {
    font-size: 16px;
    font-weight: 500;
    color: #2d2620;
    margin-bottom: 4px;
}
.card-area {
    font-size: 11px;
    color: #a8998a;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.card-desc { font-size: 13px; color: #6b5e52; line-height: 1.7; margin-bottom: 10px; }
.badge {
    display: inline-block;
    font-size: 10px;
    padding: 3px 10px;
    border-radius: 12px;
    margin-right: 5px;
    margin-bottom: 4px;
}
.badge-free { background: rgba(122,158,142,.15); color: #7a9e8e; border: 1px solid rgba(122,158,142,.3); }
.badge-paid { background: rgba(196,113,74,.12); color: #c4714a; border: 1px solid rgba(196,113,74,.25); }
.badge-mood { background: #f4efe6; color: #a8998a; border: 1px solid #ddd5c8; }
.card-price { font-size: 11px; color: #b8924a; margin-top: 8px; }

/* Section headers */
.sec-header {
    font-size: 22px;
    font-weight: 400;
    color: #2d2620;
    border-left: 3px solid #c4714a;
    padding-left: 14px;
    margin-bottom: 6px;
}
.sec-sub { font-size: 13px; color: #a8998a; margin-bottom: 20px; padding-left: 17px; }

/* PRD cards */
.prd-card {
    background: #ffffff;
    border: 1px solid #ddd5c8;
    border-radius: 14px;
    padding: 22px 24px;
    box-shadow: 0 2px 12px rgba(80,55,35,.07);
    height: 100%;
}
.prd-card h4 { color: #c4714a; font-size: 15px; margin-bottom: 10px; }
.prd-card p, .prd-card li { font-size: 13px; color: #6b5e52; line-height: 1.75; }
.step-card {
    background: #ffffff;
    border: 1px solid #ddd5c8;
    border-radius: 12px;
    padding: 18px 20px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(80,55,35,.05);
}
.step-num {
    width: 32px; height: 32px; border-radius: 50%;
    background: rgba(196,113,74,.12);
    border: 1.5px solid rgba(196,113,74,.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; color: #c4714a; font-weight: 500;
    flex-shrink: 0;
}
.tech-pill {
    display: inline-block;
    background: rgba(122,158,142,.13);
    color: #7a9e8e;
    border: 1px solid rgba(122,158,142,.3);
    border-radius: 4px;
    font-size: 11px;
    padding: 4px 12px;
    margin: 3px 4px 3px 0;
    letter-spacing: .08em;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ──
SPACES = [
    {"name": "Seoul Museum of Art (SeMA)", "area": "Seongsu", "desc": "빛으로 가득한 갤러리에서 만나는 현대미술 — 회전 전시가 끊임없이 새로운 경험을 선사해요.", "moods": ["Artistic", "Aesthetic", "Quiet"], "price": 0, "atm": 4.8, "acc": 4.5, "pop": 4.7},
    {"name": "Piknic 피크닉", "area": "Seongsu", "desc": "폐공장을 개조한 복합 문화공간 — 카페, 갤러리, 디자인 숍이 따뜻한 감성으로 어우러져 있어요.", "moods": ["Aesthetic", "Healing"], "price": 5000, "atm": 4.6, "acc": 4.2, "pop": 4.5},
    {"name": "d'strict Artspace", "area": "Seongsu", "desc": "LED 미디어 설치와 모션 반응 환경이 어우러진 몰입형 디지털 아트 공간이에요.", "moods": ["Artistic", "Aesthetic"], "price": 18000, "atm": 4.9, "acc": 4.0, "pop": 4.8},
    {"name": "대림미술관 Daelim Museum", "area": "Seongsu", "desc": "생활과 사진을 중심으로 한 아늑한 현대미술관 — 개조된 주택 건물이 매력적이에요.", "moods": ["Aesthetic", "Quiet"], "price": 5000, "atm": 4.5, "acc": 4.3, "pop": 4.2},
    {"name": "북촌한옥마을 Bukchon Hanok", "area": "Bukchon", "desc": "전통 한옥이 보존된 골목을 걷다 보면 살아있는 역사 속을 거니는 느낌이 들어요.", "moods": ["Traditional", "Healing", "Quiet"], "price": 0, "atm": 4.9, "acc": 4.0, "pop": 4.9},
    {"name": "가회민화박물관", "area": "Bukchon", "desc": "민화와 무속 유물을 소장한 소규모 사립 박물관 — 조용하고 깊이 있는 전통 예술의 세계.", "moods": ["Traditional", "Artistic"], "price": 3000, "atm": 4.4, "acc": 3.8, "pop": 3.6},
    {"name": "아라리오뮤지엄 인스페이스", "area": "Bukchon", "desc": "드라마틱한 브루탈리즘 내부가 인상적인 국제 현대미술 갤러리예요.", "moods": ["Artistic", "Quiet"], "price": 10000, "atm": 4.7, "acc": 4.2, "pop": 4.1},
    {"name": "리움미술관 Leeum", "area": "Hannam", "desc": "렘 콜하스, 마리오 보타, 장 누벨이 설계한 건물 자체가 예술인 삼성 사립 미술관.", "moods": ["Artistic", "Aesthetic", "Quiet"], "price": 0, "atm": 4.9, "acc": 4.5, "pop": 4.6},
    {"name": "Pace Gallery Seoul", "area": "Hannam", "desc": "한남동의 세련된 모더니즘 공간에 자리한 국제 블루칩 현대미술 갤러리.", "moods": ["Artistic", "Aesthetic"], "price": 0, "atm": 4.6, "acc": 4.4, "pop": 4.0},
    {"name": "국립현대미술관 MMCA", "area": "Yongsan", "desc": "한국 근현대미술의 중심 — 아름답게 복원된 역사적 건물에 자리한 국립 미술관.", "moods": ["Artistic", "Traditional", "Quiet"], "price": 4000, "atm": 4.8, "acc": 4.6, "pop": 4.7},
    {"name": "경복궁 Gyeongbokgung", "area": "Bukchon", "desc": "서울 최대의 왕궁 — 드넓은 마당과 전통 건축이 절로 발걸음을 느리게 만들어요.", "moods": ["Traditional", "Healing"], "price": 3000, "atm": 4.9, "acc": 4.7, "pop": 4.9},
    {"name": "별마당 도서관", "area": "Seongsu", "desc": "수천 권의 책이 가득한 천장 높은 아트리움 — 주변 소음이 사라지고 고요함이 찾아와요.", "moods": ["Healing", "Quiet", "Aesthetic"], "price": 0, "atm": 4.7, "acc": 4.6, "pop": 4.8},
    {"name": "커먼그라운드 Common Ground", "area": "Seongsu", "desc": "컨테이너로 만든 야외 복합공간 — 어반 아트와 감각적인 패션이 함께해요.", "moods": ["Aesthetic", "Artistic"], "price": 0, "atm": 4.3, "acc": 4.4, "pop": 4.5},
    {"name": "이태원 문화원", "area": "Itaewon", "desc": "순환 전시와 루프탑 테라스가 있는 커뮤니티 아트 허브 — 한적하고 사색적인 공간이에요.", "moods": ["Healing", "Artistic"], "price": 0, "atm": 4.2, "acc": 4.3, "pop": 3.8},
    {"name": "플래툰 쿤스트할레", "area": "Itaewon", "desc": "28개의 컨테이너로 구성된 엣지 있는 크리에이티브 공간 — 음악, 아트, 문화 이벤트가 열려요.", "moods": ["Artistic", "Aesthetic"], "price": 0, "atm": 4.4, "acc": 4.1, "pop": 4.0},
    {"name": "이화 벽화마을", "area": "Insadong", "desc": "형형색색 벽화로 가득한 언덕 골목 — 도시의 번잡함을 잊게 해주는 조용한 발견의 공간.", "moods": ["Healing", "Artistic", "Quiet"], "price": 0, "atm": 4.5, "acc": 3.7, "pop": 4.2},
    {"name": "쌈지길 Ssamziegil", "area": "Insadong", "desc": "독립 숍, 갤러리, 열린 마당이 이어지는 복합 공간 — 인사동 예술 씬의 중심이에요.", "moods": ["Aesthetic", "Artistic"], "price": 0, "atm": 4.3, "acc": 4.5, "pop": 4.6},
    {"name": "창덕궁 & 후원", "area": "Bukchon", "desc": "유네스코 세계유산 — 숨겨진 비밀 정원(후원)은 한국의 자연과 건축 이상향을 담고 있어요.", "moods": ["Traditional", "Healing", "Quiet"], "price": 8000, "atm": 4.9, "acc": 4.2, "pop": 4.8},
    {"name": "스페이스K 서울", "area": "Seongsu", "desc": "코오롱이 후원하는 열린 현대미술 공간 — 크고 넉넉한 전시장이 인상적이에요.", "moods": ["Artistic", "Quiet", "Aesthetic"], "price": 0, "atm": 4.6, "acc": 4.1, "pop": 3.9},
    {"name": "갤러리현대", "area": "Samcheong", "desc": "한국과 국제 작가를 대표하는 서울 최고(最古)의 상업 갤러리 중 하나.", "moods": ["Artistic", "Aesthetic"], "price": 0, "atm": 4.5, "acc": 4.4, "pop": 4.1},
    {"name": "국제갤러리 Kukje Gallery", "area": "Samcheong", "desc": "아름다운 조경의 복합 건물에 자리한 국제 블루칩 갤러리 — 고요하고 세련된 분위기.", "moods": ["Artistic", "Quiet"], "price": 0, "atm": 4.7, "acc": 4.3, "pop": 4.2},
    {"name": "더현대 서울 The Hyundai", "area": "Yongsan", "desc": "하늘 정원과 현대미술 설치, 몰입형 팝업 공간이 공존하는 혁신적인 백화점.", "moods": ["Aesthetic", "Healing"], "price": 0, "atm": 4.6, "acc": 4.8, "pop": 4.9},
    {"name": "서울 밤도깨비 야시장", "area": "Yongsan", "desc": "별빛 아래 먹거리·공예품·라이브 공연이 펼쳐지는 계절 야간 마켓.", "moods": ["Aesthetic", "Healing"], "price": 0, "atm": 4.7, "acc": 4.6, "pop": 4.8},
    {"name": "트릭아이뮤지엄", "area": "Hongdae", "desc": "방문자가 그림 속 주인공이 되는 트롱프뢰유 아트 뮤지엄 — 신나고 몸으로 즐기는 공간!", "moods": ["Aesthetic", "Artistic"], "price": 15000, "atm": 4.0, "acc": 4.6, "pop": 4.5},
    {"name": "홍대 아트브릿지 팝업", "area": "Hongdae", "desc": "신진 한국 작가를 소개하는 계절 팝업 갤러리 — 홍대 보행자 거리 따라 만나게 돼요.", "moods": ["Artistic", "Aesthetic"], "price": 0, "atm": 4.1, "acc": 4.7, "pop": 4.3},
    {"name": "서울사진미술관", "area": "Itaewon", "desc": "다큐멘터리부터 파인 아트까지 — 깊이 있는 사진 아카이브와 순환 전시가 인상적인 공간.", "moods": ["Quiet", "Artistic", "Aesthetic"], "price": 6000, "atm": 4.6, "acc": 4.2, "pop": 3.9},
    {"name": "한남더힐 갤러리 워크", "area": "Hannam", "desc": "한남 주거 단지 사이를 걸으며 만나는 야외 조각 정원 — 차분하고 감각적이에요.", "moods": ["Healing", "Aesthetic", "Quiet"], "price": 0, "atm": 4.5, "acc": 3.8, "pop": 4.1},
    {"name": "서울공예박물관", "area": "Bukchon", "desc": "한국 전통 공예의 아름다움을 재발견하는 박물관 — 잘 복원된 근대 건물 안에 자리해요.", "moods": ["Traditional", "Aesthetic", "Quiet"], "price": 0, "atm": 4.6, "acc": 4.3, "pop": 4.0},
]

NEIGHBORHOODS = {
    "Seongsu":   {"vibe": "🏭 Industrial Chic",   "atm": 4.5, "acc": 4.3, "pop": 4.6, "avg_price": 3000, "best": "아트+커피 데이트", "color": "#c4714a"},
    "Bukchon":   {"vibe": "⛩️ Historic Calm",     "atm": 4.8, "acc": 3.9, "pop": 4.5, "avg_price": 2000, "best": "전통 문화 탐방",   "color": "#7a9e8e"},
    "Itaewon":   {"vibe": "🌍 Cosmopolitan",       "atm": 4.2, "acc": 4.5, "pop": 4.3, "avg_price": 5000, "best": "국제 아트 씬",     "color": "#b8924a"},
    "Hannam":    {"vibe": "🎨 Refined Luxury",     "atm": 4.6, "acc": 4.3, "pop": 4.4, "avg_price": 0,    "best": "갤러리 호핑",     "color": "#d4856e"},
    "Hongdae":   {"vibe": "🎸 Youthful Energy",    "atm": 4.0, "acc": 4.7, "pop": 4.8, "avg_price": 3000, "best": "인디·스트리트 아트","color": "#8c78c3"},
    "Insadong":  {"vibe": "🖼️ Artisan Soul",       "atm": 4.4, "acc": 4.5, "pop": 4.6, "avg_price": 0,    "best": "공예·문화 체험",  "color": "#64a078"},
    "Samcheong": {"vibe": "🌸 Quiet Elegance",     "atm": 4.7, "acc": 4.2, "pop": 4.2, "avg_price": 0,    "best": "파인 아트 갤러리","color": "#a082c3"},
    "Yongsan":   {"vibe": "🏛️ Urban Grand",       "atm": 4.5, "acc": 4.7, "pop": 4.6, "avg_price": 2000, "best": "국립 박물관",     "color": "#c39b64"},
}

MOOD_EMOJI = {"Healing": "🌿", "Aesthetic": "🎨", "Quiet": "🕯️", "Artistic": "✨", "Traditional": "⛩️"}

df = pd.DataFrame(SPACES)
df["free"] = df["price"] == 0
df["moods_str"] = df["moods"].apply(lambda x: ", ".join(x))

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 🏛️ Seoul Space\n**Discovery Dashboard**")
    st.caption("Arts & Big Data · SKKU · Hyojung Park")
    st.markdown("---")
    page = st.radio(
        "페이지 선택",
        ["🗺️ Overview", "🌸 Mood Finder", "🏘️ Neighborhoods", "💰 Budget Filter", "📋 Project Info"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<div style='font-size:12px;color:#a8998a;line-height:1.8'>"
        "👩‍🎓 Hyojung Park<br>💃 Dance Major<br>📚 Arts & Big Data<br>🏫 SKKU"
        "</div>",
        unsafe_allow_html=True,
    )

# helper: render a place card
def render_card(s):
    free_badge = '<span class="badge badge-free">🎟️ 무료</span>' if s["free"] else '<span class="badge badge-paid">💳 유료</span>'
    mood_badges = "".join(f'<span class="badge badge-mood">{MOOD_EMOJI.get(m,"")} {m}</span>' for m in s["moods"])
    price_txt = "🎟️ 무료 입장" if s["free"] else f"💳 ₩{s['price']:,}"
    st.markdown(f"""
    <div class="place-card">
        <div class="card-title">{s['name']} {free_badge}</div>
        <div class="card-area">📍 {s['area']}</div>
        <div class="card-desc">{s['desc']}</div>
        <div>{mood_badges}</div>
        <div class="card-price">{price_txt} &nbsp;·&nbsp; ⭐ 분위기 {s['atm']}/5</div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════
if page == "🗺️ Overview":
    st.markdown('<div class="sec-header">🗺️ Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">서울 문화공간 전체 현황을 한눈에 살펴보세요</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏛️ Cultural Spaces", len(df))
    c2.metric("📍 Neighborhoods", df["area"].nunique())
    c3.metric("🎟️ Free Entry", f"{int(df['free'].mean()*100)}%")
    c4.metric("⭐ Avg Atmosphere", f"{df['atm'].mean():.1f}")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### 📊 동네별 공간 수")
        nb_counts = df.groupby("area").size().reset_index(name="count")
        colors = [NEIGHBORHOODS.get(a, {}).get("color", "#c4714a") for a in nb_counts["area"]]
        fig_bar = px.bar(
            nb_counts, x="area", y="count",
            color="area",
            color_discrete_map={a: NEIGHBORHOODS.get(a, {}).get("color", "#c4714a") for a in nb_counts["area"]},
            labels={"area": "동네", "count": "공간 수"},
        )
        fig_bar.update_layout(
            plot_bgcolor="#faf7f2", paper_bgcolor="#ffffff",
            font_color="#6b5e52", showlegend=False,
            margin=dict(t=10, b=10), height=280,
        )
        fig_bar.update_traces(marker_line_width=0)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown("#### 🌈 무드 분포")
        all_moods = [m for ms in df["moods"] for m in ms]
        mood_counts = pd.Series(all_moods).value_counts().reset_index()
        mood_counts.columns = ["mood", "count"]
        mood_counts["label"] = mood_counts["mood"].apply(lambda m: f"{MOOD_EMOJI.get(m,'')} {m}")
        fig_pie = px.pie(
            mood_counts, names="label", values="count",
            color_discrete_sequence=["#7a9e8e", "#c4714a", "#b8a0d0", "#d4856e", "#b8924a"],
            hole=0.5,
        )
        fig_pie.update_layout(
            plot_bgcolor="#faf7f2", paper_bgcolor="#ffffff",
            font_color="#6b5e52", margin=dict(t=10, b=10), height=280,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("#### 💳 입장료 분포")
    bins = ["무료", "₩1–5k", "₩5–10k", "₩10–20k", "₩20k+"]
    bin_counts = [
        len(df[df["price"] == 0]),
        len(df[(df["price"] > 0) & (df["price"] <= 5000)]),
        len(df[(df["price"] > 5000) & (df["price"] <= 10000)]),
        len(df[(df["price"] > 10000) & (df["price"] <= 20000)]),
        len(df[df["price"] > 20000]),
    ]
    fig_price = px.bar(
        x=bins, y=bin_counts,
        color=bins,
        color_discrete_sequence=["#7a9e8e", "#b8924a", "#c4714a", "#d4856e", "#b8a0c8"],
        labels={"x": "가격대", "y": "공간 수"},
    )
    fig_price.update_layout(
        plot_bgcolor="#faf7f2", paper_bgcolor="#ffffff",
        font_color="#6b5e52", showlegend=False,
        margin=dict(t=10, b=10), height=260,
    )
    fig_price.update_traces(marker_line_width=0)
    st.plotly_chart(fig_price, use_container_width=True)


# ════════════════════════════════
# PAGE: MOOD FINDER
# ════════════════════════════════
elif page == "🌸 Mood Finder":
    st.markdown('<div class="sec-header">🌸 Mood Finder</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">오늘의 기분에 맞는 서울 문화공간을 찾아보세요 ✨</div>', unsafe_allow_html=True)

    st.info("💡 공간의 분위기가 몸의 움직임을 먼저 만들어냅니다 — Dance & Space 연구에서 영감을 받았어요.", icon="💃")

    mood_options = ["🌿 Healing", "🎨 Aesthetic", "🕯️ Quiet", "✨ Artistic", "⛩️ Traditional"]
    selected = st.multiselect(
        "무드를 선택하세요 (복수 선택 가능)",
        mood_options,
        default=["🌿 Healing"],
    )

    selected_keys = [s.split(" ", 1)[1] for s in selected]

    filtered = [s for s in SPACES if any(m in s["moods"] for m in selected_keys)]

    if not filtered:
        st.warning("해당 무드의 공간이 없어요 😢 다른 무드를 선택해보세요!")
    else:
        st.success(f"✅ **{len(filtered)}개** 공간을 찾았어요!")
        col1, col2 = st.columns(2)
        for i, s in enumerate(filtered):
            with (col1 if i % 2 == 0 else col2):
                render_card(s)


# ════════════════════════════════
# PAGE: NEIGHBORHOODS
# ════════════════════════════════
elif page == "🏘️ Neighborhoods":
    st.markdown('<div class="sec-header">🏘️ Neighborhood 비교</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">분위기, 접근성, 인기도를 기준으로 서울의 문화 동네를 비교해보세요 🗺️</div>', unsafe_allow_html=True)

    all_nbs = list(NEIGHBORHOODS.keys())
    selected_nbs = st.multiselect(
        "비교할 동네를 선택하세요",
        all_nbs,
        default=["Seongsu", "Bukchon", "Itaewon", "Hannam"],
    )

    if len(selected_nbs) < 2:
        st.warning("동네를 2개 이상 선택해주세요!")
    else:
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("#### 🕸️ Atmosphere · Accessibility · Popularity")
            categories = ["Atmosphere", "Accessibility", "Popularity"]
            fig_radar = go.Figure()
            for nb in selected_nbs:
                d = NEIGHBORHOODS[nb]
                fig_radar.add_trace(go.Scatterpolar(
                    r=[d["atm"], d["acc"], d["pop"]],
                    theta=categories,
                    fill="toself",
                    name=nb,
                    line_color=d["color"],
                    fillcolor=d["color"].replace(")", ", 0.08)").replace("rgb", "rgba") if "rgb" in d["color"] else d["color"] + "15",
                ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[3.5, 5], tickfont_color="#a8998a"),
                    angularaxis=dict(tickfont_color="#6b5e52"),
                    bgcolor="#faf7f2",
                ),
                paper_bgcolor="#ffffff", font_color="#6b5e52",
                legend=dict(font_color="#6b5e52"),
                margin=dict(t=20, b=20), height=340,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_r:
            st.markdown("#### 📈 Popularity vs Accessibility")
            scatter_data = [{"name": nb, "acc": NEIGHBORHOODS[nb]["acc"], "pop": NEIGHBORHOODS[nb]["pop"], "color": NEIGHBORHOODS[nb]["color"]} for nb in selected_nbs]
            fig_scatter = go.Figure()
            for d in scatter_data:
                fig_scatter.add_trace(go.Scatter(
                    x=[d["acc"]], y=[d["pop"]],
                    mode="markers+text",
                    name=d["name"],
                    text=[d["name"]],
                    textposition="top center",
                    marker=dict(size=18, color=d["color"], line=dict(width=2, color="#ffffff")),
                ))
            fig_scatter.update_layout(
                xaxis=dict(title="Accessibility", range=[3.4, 5.1], gridcolor="#ede6d9"),
                yaxis=dict(title="Popularity",    range=[3.4, 5.1], gridcolor="#ede6d9"),
                plot_bgcolor="#faf7f2", paper_bgcolor="#ffffff",
                font_color="#6b5e52", showlegend=False,
                margin=dict(t=20, b=20), height=340,
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("#### 📋 상세 데이터")
        table_rows = []
        for nb in selected_nbs:
            d = NEIGHBORHOODS[nb]
            table_rows.append({
                "동네": nb,
                "분위기": d["vibe"],
                "Atmosphere ⭐": d["atm"],
                "Accessibility 🚇": d["acc"],
                "Popularity 🔥": d["pop"],
                "평균 입장료": "무료" if d["avg_price"] == 0 else f"₩{d['avg_price']:,}",
                "추천 목적": d["best"],
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        st.markdown("#### 🗂️ 선택된 동네의 공간")
        nb_filtered = [s for s in SPACES if s["area"] in selected_nbs]
        col1, col2 = st.columns(2)
        for i, s in enumerate(nb_filtered):
            with (col1 if i % 2 == 0 else col2):
                render_card(s)


# ════════════════════════════════
# PAGE: BUDGET FILTER
# ════════════════════════════════
elif page == "💰 Budget Filter":
    st.markdown('<div class="sec-header">💰 Budget Filter</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">예산에 맞는 서울 문화공간을 찾아보세요 💳</div>', unsafe_allow_html=True)

    col_sl, col_mood = st.columns([2, 1])
    with col_sl:
        budget = st.slider("최대 예산 (₩)", 0, 30000, 15000, step=1000,
                           format="₩%d")
    with col_mood:
        mood_filter = st.selectbox(
            "무드 필터",
            ["모든 무드"] + [f"{MOOD_EMOJI[m]} {m}" for m in MOOD_EMOJI],
        )

    mood_key = None if mood_filter == "모든 무드" else mood_filter.split(" ", 1)[1]
    filtered = [s for s in SPACES if s["price"] <= budget]
    if mood_key:
        filtered = [s for s in filtered if mood_key in s["moods"]]

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### 📈 예산별 이용 가능 공간")
        thresholds = [0, 3000, 5000, 8000, 10000, 15000, 20000, 30000]
        counts_by_budget = [len([s for s in SPACES if s["price"] <= t]) for t in thresholds]
        fig_line = px.line(
            x=[t if t > 0 else "Free" for t in thresholds],
            y=counts_by_budget,
            markers=True,
            labels={"x": "예산", "y": "공간 수"},
            color_discrete_sequence=["#c4714a"],
        )
        fig_line.update_traces(line_width=2.5, marker_size=8)
        fig_line.update_layout(
            plot_bgcolor="#faf7f2", paper_bgcolor="#ffffff",
            font_color="#6b5e52", margin=dict(t=10, b=10), height=260,
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_r:
        st.markdown("#### 💳 가격대별 공간 수")
        tier_labels = ["🎟️ Free", "~₩5k", "₩5–10k", "₩10k+"]
        tier_counts = [
            len(df[df["price"] == 0]),
            len(df[(df["price"] > 0) & (df["price"] <= 5000)]),
            len(df[(df["price"] > 5000) & (df["price"] <= 10000)]),
            len(df[df["price"] > 10000]),
        ]
        fig_tier = px.bar(
            x=tier_labels, y=tier_counts,
            color=tier_labels,
            color_discrete_sequence=["#7a9e8e", "#b8924a", "#c4714a", "#d4856e"],
            labels={"x": "가격대", "y": "공간 수"},
        )
        fig_tier.update_layout(
            plot_bgcolor="#faf7f2", paper_bgcolor="#ffffff",
            font_color="#6b5e52", showlegend=False,
            margin=dict(t=10, b=10), height=260,
        )
        fig_tier.update_traces(marker_line_width=0)
        st.plotly_chart(fig_tier, use_container_width=True)

    budget_label = "무료 공간만" if budget == 0 else f"₩{budget:,} 이하"
    st.success(f"✅ **{budget_label}** 기준 — **{len(filtered)}개** 공간을 이용할 수 있어요!")
    filtered_sorted = sorted(filtered, key=lambda s: s["price"])
    col1, col2 = st.columns(2)
    for i, s in enumerate(filtered_sorted):
        with (col1 if i % 2 == 0 else col2):
            render_card(s)


# ════════════════════════════════
# PAGE: PROJECT INFO (PRD)
# ════════════════════════════════
elif page == "📋 Project Info":
    st.markdown('<div class="sec-header">📋 Project Info (PRD)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Seoul Exhibition & Space Discovery Dashboard — 프로젝트 소개</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="prd-card">
            <h4>❓ Why — 프로젝트 목적</h4>
            <p>인기 순위가 아닌 무드·분위기·예산에 맞는 서울의 전시·문화 공간을 찾을 수 있도록 돕기 위한 프로젝트예요. 전시 데이트 코스를 고민하는 사람들에게 데이터 시각화를 통한 개인화된 추천을 제공합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="prd-card">
            <h4>👥 Who — 대상 사용자</h4>
            <ul>
                <li>🧑‍🎨 20대 청년 및 전시 애호가</li>
                <li>💑 데이트 코스를 찾는 커플</li>
                <li>🌸 감각적인 공간에 관심 있는 사람</li>
                <li>🗺️ 서울 문화·예술 씬이 궁금한 누구나</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
        <div class="prd-card">
            <h4>🛠️ What — 핵심 기능</h4>
            <ul>
                <li>🌿 무드 기반 추천 시스템</li>
                <li>🏘️ 동네 비교 툴 (성수, 북촌, 이태원, 한남…)</li>
                <li>💰 예산 기반 추천</li>
                <li>📊 인터랙티브 데이터 시각화</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="prd-card">
            <h4>⚙️ How — 기술 스택</h4>
            <p>
                <span class="tech-pill">Python 3.9+</span>
                <span class="tech-pill">Streamlit</span>
                <span class="tech-pill">Pandas</span>
                <span class="tech-pill">Plotly</span>
                <span class="tech-pill">GitHub</span>
                <span class="tech-pill">Streamlit Cloud</span>
            </p>
            <p style="margin-top:12px">Python과 Streamlit 라이브러리를 활용하고, 전시 장소·문화 공간·예산 정보를 담은 큐레이션 데이터셋을 사용합니다.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🗓️ 3-Step Build Plan")
    st.markdown("""
    <div class="step-card">
        <div class="step-num">1</div>
        <div>
            <strong>🏗️ Basic UI Layout & Sample Dataset Setup</strong><br>
            <span style="font-size:13px;color:#6b5e52">GitHub 저장소 생성 및 Streamlit 환경 설정. 서울 전시·문화공간 샘플 데이터셋 준비. 홈화면 및 네비게이션 레이아웃 디자인.</span>
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">2</div>
        <div>
            <strong>🔮 Interactive Recommendation & Visualization</strong><br>
            <span style="font-size:13px;color:#6b5e52">무드 기반 필터 구현. 예산 및 동네 비교 기능 추가. Plotly를 활용한 차트 시각화 적용.</span>
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">3</div>
        <div>
            <strong>✨ UI Improvement & Real Data Integration</strong><br>
            <span style="font-size:13px;color:#6b5e52">깔끔하고 모던한 디자인 테마 적용. 실제 전시·문화공간 데이터 추가. 반응형 개선 및 배포 완료.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="prd-card">
        <h4>💃 Academic & Creative Value</h4>
        <p>무용 전공자로서 공간·분위기·감정 경험의 관계에 대한 관심이 담긴 프로젝트입니다. 전시 및 문화공간 데이터를 인터랙티브 추천 시스템으로 구성함으로써, 주관적 감각을 데이터 기반 문화 경험으로 전환하는 새로운 방식으로 서울의 예술·전시 씬을 탐색할 수 있도록 합니다. 🌿</p>
    </div>
    """, unsafe_allow_html=True)
