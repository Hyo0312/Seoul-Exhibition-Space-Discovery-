import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Seoul Space Discovery",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500&family=Noto+Sans+SC:wght@300;400;500&family=Noto+Sans+JP:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', 'Noto Sans SC', 'Noto Sans JP', sans-serif; }
.main { background-color: #faf7f2; }
[data-testid="stSidebar"] { background-color: #f4efe6; border-right: 1px solid #ddd5c8; }
div[data-testid="metric-container"] { background:#fff; border:1px solid #ddd5c8; border-radius:12px; padding:16px 20px; box-shadow:0 2px 12px rgba(80,55,35,.07); }
div[data-testid="metric-container"] label { color:#a8998a !important; font-size:11px !important; letter-spacing:.12em; text-transform:uppercase; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color:#c4714a !important; font-size:2rem !important; }
.place-card { background:#fff; border:1.5px solid #ddd5c8; border-radius:14px; padding:20px 22px; margin-bottom:14px; box-shadow:0 2px 12px rgba(80,55,35,.07); }
.card-title { font-size:16px; font-weight:500; color:#2d2620; margin-bottom:4px; }
.card-area  { font-size:11px; color:#a8998a; letter-spacing:.1em; text-transform:uppercase; margin-bottom:8px; }
.card-desc  { font-size:13px; color:#6b5e52; line-height:1.7; margin-bottom:10px; }
.badge { display:inline-block; font-size:10px; padding:3px 10px; border-radius:12px; margin-right:5px; margin-bottom:4px; }
.badge-free { background:rgba(122,158,142,.15); color:#7a9e8e; border:1px solid rgba(122,158,142,.3); }
.badge-paid { background:rgba(196,113,74,.12);  color:#c4714a; border:1px solid rgba(196,113,74,.25); }
.badge-mood { background:#f4efe6; color:#a8998a; border:1px solid #ddd5c8; }
.card-price { font-size:11px; color:#b8924a; margin-top:8px; }
.sec-header { font-size:22px; font-weight:400; color:#2d2620; border-left:3px solid #c4714a; padding-left:14px; margin-bottom:6px; }
.sec-sub    { font-size:13px; color:#a8998a; margin-bottom:20px; padding-left:17px; }
.prd-card { background:#fff; border:1px solid #ddd5c8; border-radius:14px; padding:22px 24px; box-shadow:0 2px 12px rgba(80,55,35,.07); }
.prd-card h4 { color:#c4714a; font-size:15px; margin-bottom:10px; }
.prd-card p, .prd-card li { font-size:13px; color:#6b5e52; line-height:1.75; }
.step-card { background:#fff; border:1px solid #ddd5c8; border-radius:12px; padding:18px 20px; margin-bottom:12px; box-shadow:0 2px 8px rgba(80,55,35,.05); }
.step-num { display:inline-flex; align-items:center; justify-content:center; width:32px; height:32px; border-radius:50%; background:rgba(196,113,74,.12); border:1.5px solid rgba(196,113,74,.3); font-size:13px; color:#c4714a; font-weight:500; flex-shrink:0; margin-right:14px; }
.tech-pill { display:inline-block; background:rgba(122,158,142,.13); color:#7a9e8e; border:1px solid rgba(122,158,142,.3); border-radius:4px; font-size:11px; padding:4px 12px; margin:3px 4px 3px 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════
T = {
    "🇰🇷 한국어": {
        "app_title": "### 🏛️ Seoul Space\n**Discovery Dashboard**",
        "app_caption": "Arts & Big Data · SKKU · Hyojung Park",
        "lang_label": "언어 선택",
        "page_label": "페이지",
        "pages": ["🗺️ Overview", "🌸 Mood Finder", "🏘️ Neighborhoods", "💰 Budget Filter", "📋 Project Info"],
        "sidebar_info": "👩‍🎓 Hyojung Park<br>💃 Dance Major<br>📚 Arts & Big Data<br>🏫 SKKU",

        # Overview
        "ov_header": "🗺️ Overview",
        "ov_sub": "서울 문화공간 전체 현황을 한눈에 살펴보세요",
        "ov_m1": "🏛️ Cultural Spaces", "ov_m2": "📍 Neighborhoods",
        "ov_m3": "🎟️ Free Entry", "ov_m4": "⭐ Avg Atmosphere",
        "ov_c1": "#### 📊 동네별 공간 수", "ov_c2": "#### 🌈 무드 분포",
        "ov_c3": "#### 💳 입장료 분포",
        "ov_bar_x": "동네", "ov_bar_y": "공간 수",
        "ov_price_x": "가격대",

        # Mood
        "mood_header": "🌸 Mood Finder",
        "mood_sub": "오늘의 기분에 맞는 서울 문화공간을 찾아보세요 ✨",
        "mood_info": "💡 공간의 분위기가 몸의 움직임을 먼저 만들어냅니다 — Dance & Space 연구에서 영감을 받았어요.",
        "mood_select": "무드를 선택하세요 (복수 선택 가능)",
        "mood_opts": ["🌿 Healing", "🎨 Aesthetic", "🕯️ Quiet", "✨ Artistic", "⛩️ Traditional"],
        "mood_none": "해당 무드의 공간이 없어요 😢 다른 무드를 선택해보세요!",
        "mood_found": "개 공간을 찾았어요!",

        # Neighborhood
        "nb_header": "🏘️ Neighborhood 비교",
        "nb_sub": "분위기, 접근성, 인기도를 기준으로 서울의 문화 동네를 비교해보세요 🗺️",
        "nb_select": "비교할 동네를 선택하세요",
        "nb_warn": "동네를 2개 이상 선택해주세요!",
        "nb_radar": "#### 🕸️ Atmosphere · Accessibility · Popularity",
        "nb_scatter": "#### 📈 Popularity vs Accessibility",
        "nb_table": "#### 📋 상세 데이터",
        "nb_cards": "#### 🗂️ 선택된 동네의 공간",
        "nb_cols": ["동네","분위기","Atmosphere ⭐","Accessibility 🚇","Popularity 🔥","평균 입장료","추천 목적"],
        "nb_free": "무료",

        # Budget
        "bud_header": "💰 Budget Filter",
        "bud_sub": "예산에 맞는 서울 문화공간을 찾아보세요 💳",
        "bud_slider": "최대 예산 (₩)",
        "bud_mood": "무드 필터",
        "bud_all": "모든 무드",
        "bud_line": "#### 📈 예산별 이용 가능 공간",
        "bud_bar": "#### 💳 가격대별 공간 수",
        "bud_line_x": "예산", "bud_line_y": "공간 수",
        "bud_free_only": "무료 공간만",
        "bud_result": "기준 —",
        "bud_result2": "개 공간을 이용할 수 있어요!",

        # PRD
        "prd_header": "📋 Project Info (PRD)",
        "prd_sub": "Seoul Exhibition & Space Discovery Dashboard — 프로젝트 소개",
        "prd_why_t": "❓ Why — 프로젝트 목적",
        "prd_why_b": "인기 순위가 아닌 무드·분위기·예산에 맞는 서울의 전시·문화 공간을 찾을 수 있도록 돕기 위한 프로젝트예요. 전시 데이트 코스를 고민하는 사람들에게 데이터 시각화를 통한 개인화된 추천을 제공합니다.",
        "prd_who_t": "👥 Who — 대상 사용자",
        "prd_who_b": ["🧑‍🎨 20대 청년 및 전시 애호가","💑 데이트 코스를 찾는 커플","🌸 감각적인 공간에 관심 있는 사람","🗺️ 서울 문화·예술 씬이 궁금한 누구나"],
        "prd_what_t": "🛠️ What — 핵심 기능",
        "prd_what_b": ["🌿 무드 기반 추천 시스템","🏘️ 동네 비교 툴 (성수, 북촌, 이태원, 한남…)","💰 예산 기반 추천","📊 인터랙티브 데이터 시각화"],
        "prd_how_t": "⚙️ How — 기술 스택",
        "prd_how_b": "Python과 Streamlit 라이브러리를 활용하고, 전시 장소·문화 공간·예산 정보를 담은 큐레이션 데이터셋을 사용합니다.",
        "prd_steps_t": "#### 🗓️ 3-Step Build Plan",
        "prd_steps": [
            ("1","🏗️ Basic UI Layout & Sample Dataset Setup","GitHub 저장소 생성 및 Streamlit 환경 설정. 서울 전시·문화공간 샘플 데이터셋 준비. 홈화면 및 네비게이션 레이아웃 디자인."),
            ("2","🔮 Interactive Recommendation & Visualization","무드 기반 필터 구현. 예산 및 동네 비교 기능 추가. Plotly를 활용한 차트 시각화 적용."),
            ("3","✨ UI Improvement & Real Data Integration","깔끔하고 모던한 디자인 테마 적용. 실제 전시·문화공간 데이터 추가. 반응형 개선 및 배포 완료."),
        ],
        "prd_val_t": "💃 Academic & Creative Value",
        "prd_val_b": "무용 전공자로서 공간·분위기·감정 경험의 관계에 대한 관심이 담긴 프로젝트입니다. 전시 및 문화공간 데이터를 인터랙티브 추천 시스템으로 구성함으로써, 주관적 감각을 데이터 기반 문화 경험으로 전환하는 새로운 방식으로 서울의 예술·전시 씬을 탐색할 수 있도록 합니다. 🌿",

        # Card
        "card_free": "🎟️ 무료", "card_paid": "💳 유료",
        "card_free_txt": "🎟️ 무료 입장", "card_atm": "분위기",
    },

    "🇨🇳 中文": {
        "app_title": "### 🏛️ Seoul Space\n**发现仪表板**",
        "app_caption": "艺术与大数据 · 成均馆大学 · 朴孝静",
        "lang_label": "语言选择",
        "page_label": "页面",
        "pages": ["🗺️ 总览", "🌸 心情推荐", "🏘️ 街区比较", "💰 预算筛选", "📋 项目简介"],
        "sidebar_info": "👩‍🎓 朴孝静<br>💃 舞蹈专业<br>📚 艺术与大数据<br>🏫 成均馆大学",

        "ov_header": "🗺️ 总览",
        "ov_sub": "一览首尔文化空间全貌",
        "ov_m1": "🏛️ 文化空间", "ov_m2": "📍 街区数量",
        "ov_m3": "🎟️ 免费比例", "ov_m4": "⭐ 平均氛围",
        "ov_c1": "#### 📊 各街区空间数量", "ov_c2": "#### 🌈 心情分布",
        "ov_c3": "#### 💳 门票价格分布",
        "ov_bar_x": "街区", "ov_bar_y": "空间数量",
        "ov_price_x": "价格区间",

        "mood_header": "🌸 心情推荐",
        "mood_sub": "找到符合今天心情的首尔文化空间 ✨",
        "mood_info": "💡 空间的氛围决定了身体的动作 — 来自舞蹈与空间研究的灵感。",
        "mood_select": "选择心情（可多选）",
        "mood_opts": ["🌿 治愈", "🎨 美感", "🕯️ 静谧", "✨ 艺术", "⛩️ 传统"],
        "mood_none": "没有符合该心情的空间 😢 请尝试其他心情！",
        "mood_found": "个空间",

        "nb_header": "🏘️ 街区比较",
        "nb_sub": "根据氛围、便利性和人气比较首尔各文化街区 🗺️",
        "nb_select": "选择要比较的街区",
        "nb_warn": "请至少选择2个街区！",
        "nb_radar": "#### 🕸️ 氛围 · 便利性 · 人气",
        "nb_scatter": "#### 📈 人气 vs 便利性",
        "nb_table": "#### 📋 详细数据",
        "nb_cards": "#### 🗂️ 所选街区的空间",
        "nb_cols": ["街区","氛围","氛围评分 ⭐","便利性 🚇","人气 🔥","平均门票","推荐用途"],
        "nb_free": "免费",

        "bud_header": "💰 预算筛选",
        "bud_sub": "找到符合预算的首尔文化空间 💳",
        "bud_slider": "最大预算 (₩)",
        "bud_mood": "心情筛选",
        "bud_all": "全部心情",
        "bud_line": "#### 📈 各预算可用空间数",
        "bud_bar": "#### 💳 价格区间分布",
        "bud_line_x": "预算", "bud_line_y": "空间数量",
        "bud_free_only": "仅免费空间",
        "bud_result": "预算内共有",
        "bud_result2": "个空间可选！",

        "prd_header": "📋 项目简介 (PRD)",
        "prd_sub": "首尔展览与空间发现仪表板 — 项目介绍",
        "prd_why_t": "❓ Why — 项目目的",
        "prd_why_b": "本项目旨在帮助用户根据心情、氛围和预算发现首尔的展览和文化空间，而不仅仅是选择热门地点。为烦恼约会去哪的用户，通过数据可视化提供个性化推荐。",
        "prd_who_t": "👥 Who — 目标用户",
        "prd_who_b": ["🧑‍🎨 20多岁年轻人及展览爱好者","💑 寻找约会路线的情侣","🌸 对美感空间感兴趣的人","🗺️ 对首尔文化艺术圈感兴趣的所有人"],
        "prd_what_t": "🛠️ What — 核心功能",
        "prd_what_b": ["🌿 基于心情的推荐系统","🏘️ 街区比较工具（圣水、北村、梨泰院、汉南…）","💰 基于预算的推荐","📊 交互式数据可视化"],
        "prd_how_t": "⚙️ How — 技术栈",
        "prd_how_b": "使用Python和Streamlit库，利用包含展览地点、文化空间和预算信息的精选数据集。",
        "prd_steps_t": "#### 🗓️ 三步开发计划",
        "prd_steps": [
            ("1","🏗️ 基础UI布局与样本数据集","创建GitHub仓库并设置Streamlit环境。准备首尔展览和文化空间样本数据集。设计主页和导航布局。"),
            ("2","🔮 交互式推荐与可视化","实现基于心情的筛选器。添加预算和街区比较功能。使用Plotly实现图表可视化。"),
            ("3","✨ UI优化与真实数据集成","应用简洁现代的设计主题。添加真实展览和文化空间数据。改善响应式设计并完成部署。"),
        ],
        "prd_val_t": "💃 学术与创意价值",
        "prd_val_b": "作为舞蹈专业学生，本项目反映了对空间、氛围与情感体验关系的兴趣。通过将展览和文化空间数据组织成交互式推荐系统，将主观感受转化为数据驱动的文化体验。🌿",

        "card_free": "🎟️ 免费", "card_paid": "💳 付费",
        "card_free_txt": "🎟️ 免费入场", "card_atm": "氛围",
    },

    "🇺🇸 English": {
        "app_title": "### 🏛️ Seoul Space\n**Discovery Dashboard**",
        "app_caption": "Arts & Big Data · SKKU · Hyojung Park",
        "lang_label": "Language",
        "page_label": "Page",
        "pages": ["🗺️ Overview", "🌸 Mood Finder", "🏘️ Neighborhoods", "💰 Budget Filter", "📋 Project Info"],
        "sidebar_info": "👩‍🎓 Hyojung Park<br>💃 Dance Major<br>📚 Arts & Big Data<br>🏫 SKKU",

        "ov_header": "🗺️ Overview",
        "ov_sub": "Explore Seoul's cultural spaces at a glance",
        "ov_m1": "🏛️ Cultural Spaces", "ov_m2": "📍 Neighborhoods",
        "ov_m3": "🎟️ Free Entry", "ov_m4": "⭐ Avg Atmosphere",
        "ov_c1": "#### 📊 Spaces by Neighborhood", "ov_c2": "#### 🌈 Mood Distribution",
        "ov_c3": "#### 💳 Entry Price Distribution",
        "ov_bar_x": "Neighborhood", "ov_bar_y": "Number of Spaces",
        "ov_price_x": "Price Range",

        "mood_header": "🌸 Mood Finder",
        "mood_sub": "Find Seoul cultural spaces that match your mood today ✨",
        "mood_info": "💡 The atmosphere of a space shapes the body's movement first — inspired by Dance & Space research.",
        "mood_select": "Select your mood (multiple selection)",
        "mood_opts": ["🌿 Healing", "🎨 Aesthetic", "🕯️ Quiet", "✨ Artistic", "⛩️ Traditional"],
        "mood_none": "No spaces match this mood 😢 Try another!",
        "mood_found": "spaces found!",

        "nb_header": "🏘️ Neighborhood Comparison",
        "nb_sub": "Compare Seoul's cultural districts by atmosphere, accessibility & popularity 🗺️",
        "nb_select": "Select neighborhoods to compare",
        "nb_warn": "Please select at least 2 neighborhoods!",
        "nb_radar": "#### 🕸️ Atmosphere · Accessibility · Popularity",
        "nb_scatter": "#### 📈 Popularity vs Accessibility",
        "nb_table": "#### 📋 Detailed Data",
        "nb_cards": "#### 🗂️ Spaces in Selected Neighborhoods",
        "nb_cols": ["Neighborhood","Vibe","Atmosphere ⭐","Accessibility 🚇","Popularity 🔥","Avg Price","Best For"],
        "nb_free": "Free",

        "bud_header": "💰 Budget Filter",
        "bud_sub": "Find cultural spaces within your budget 💳",
        "bud_slider": "Max Budget (₩)",
        "bud_mood": "Mood Filter",
        "bud_all": "All Moods",
        "bud_line": "#### 📈 Available Spaces by Budget",
        "bud_bar": "#### 💳 Price Tier Breakdown",
        "bud_line_x": "Budget", "bud_line_y": "Number of Spaces",
        "bud_free_only": "Free only",
        "bud_result": "Budget —",
        "bud_result2": "spaces available!",

        "prd_header": "📋 Project Info (PRD)",
        "prd_sub": "Seoul Exhibition & Space Discovery Dashboard — Project Introduction",
        "prd_why_t": "❓ Why — Project Purpose",
        "prd_why_b": "This project helps users discover exhibitions and cultural spaces in Seoul based on mood, atmosphere, and budget rather than simply choosing popular places. It provides personalized recommendations through data visualization for people struggling to decide where to go.",
        "prd_who_t": "👥 Who — Target Users",
        "prd_who_b": ["🧑‍🎨 People in their 20s & exhibition enthusiasts","💑 Couples searching for date courses","🌸 People interested in aesthetic cultural spaces","🗺️ Anyone curious about Seoul's art & culture scene"],
        "prd_what_t": "🛠️ What — Key Features",
        "prd_what_b": ["🌿 Mood-Based Recommendation System","🏘️ Neighborhood Comparison Tool (Seongsu, Bukchon, Itaewon, Hannam…)","💰 Budget-Based Recommendation","📊 Interactive Data Visualization"],
        "prd_how_t": "⚙️ How — Tech Stack",
        "prd_how_b": "Built using Python and the Streamlit library, utilizing curated datasets of exhibition locations, cultural venues, and budget information.",
        "prd_steps_t": "#### 🗓️ 3-Step Build Plan",
        "prd_steps": [
            ("1","🏗️ Basic UI Layout & Sample Dataset Setup","Create GitHub repository and Streamlit environment. Prepare sample dataset of Seoul cultural spaces. Design homepage and navigation layout."),
            ("2","🔮 Interactive Recommendation & Visualization","Create mood-based filters. Add budget and neighborhood comparison functions. Implement charts using Plotly."),
            ("3","✨ UI Improvement & Real Data Integration","Apply clean modern design theme. Add real exhibition and cultural space data. Improve responsiveness and deploy."),
        ],
        "prd_val_t": "💃 Academic & Creative Value",
        "prd_val_b": "As a Dance major, this project reflects an interest in the relationship between space, atmosphere, and emotional experience. By organizing cultural space data into an interactive recommendation system, it transforms subjective feelings into data-driven cultural experiences. 🌿",

        "card_free": "🎟️ Free", "card_paid": "💳 Paid",
        "card_free_txt": "🎟️ Free Entry", "card_atm": "Atmosphere",
    },

    "🇯🇵 日本語": {
        "app_title": "### 🏛️ Seoul Space\n**ディスカバリー**",
        "app_caption": "アート＆ビッグデータ · 成均館大学 · パク・ヒョジョン",
        "lang_label": "言語選択",
        "page_label": "ページ",
        "pages": ["🗺️ 概要", "🌸 気分検索", "🏘️ エリア比較", "💰 予算フィルター", "📋 プロジェクト情報"],
        "sidebar_info": "👩‍🎓 パク・ヒョジョン<br>💃 舞踊専攻<br>📚 アート＆ビッグデータ<br>🏫 成均館大学",

        "ov_header": "🗺️ 概要",
        "ov_sub": "ソウルの文化スペース全体を一目で確認",
        "ov_m1": "🏛️ 文化スペース", "ov_m2": "📍 エリア数",
        "ov_m3": "🎟️ 無料入場", "ov_m4": "⭐ 平均雰囲気",
        "ov_c1": "#### 📊 エリア別スペース数", "ov_c2": "#### 🌈 気分の分布",
        "ov_c3": "#### 💳 入場料の分布",
        "ov_bar_x": "エリア", "ov_bar_y": "スペース数",
        "ov_price_x": "価格帯",

        "mood_header": "🌸 気分検索",
        "mood_sub": "今日の気分に合ったソウルの文化スペースを探しましょう ✨",
        "mood_info": "💡 空間の雰囲気が身体の動きを先に作ります — ダンス＆スペース研究からのインスピレーション。",
        "mood_select": "気分を選んでください（複数選択可）",
        "mood_opts": ["🌿 ヒーリング", "🎨 審美的", "🕯️ 静寂", "✨ 芸術的", "⛩️ 伝統的"],
        "mood_none": "この気分に合うスペースがありません 😢 別の気分をお試しください！",
        "mood_found": "件のスペースが見つかりました！",

        "nb_header": "🏘️ エリア比較",
        "nb_sub": "雰囲気・アクセス・人気度でソウルの文化エリアを比較 🗺️",
        "nb_select": "比較するエリアを選択",
        "nb_warn": "2つ以上のエリアを選択してください！",
        "nb_radar": "#### 🕸️ 雰囲気 · アクセス · 人気度",
        "nb_scatter": "#### 📈 人気度 vs アクセス",
        "nb_table": "#### 📋 詳細データ",
        "nb_cards": "#### 🗂️ 選択エリアのスペース",
        "nb_cols": ["エリア","雰囲気","雰囲気 ⭐","アクセス 🚇","人気度 🔥","平均入場料","おすすめ用途"],
        "nb_free": "無料",

        "bud_header": "💰 予算フィルター",
        "bud_sub": "予算に合ったソウルの文化スペースを探しましょう 💳",
        "bud_slider": "最大予算 (₩)",
        "bud_mood": "気分フィルター",
        "bud_all": "すべての気分",
        "bud_line": "#### 📈 予算別利用可能スペース数",
        "bud_bar": "#### 💳 価格帯別スペース数",
        "bud_line_x": "予算", "bud_line_y": "スペース数",
        "bud_free_only": "無料のみ",
        "bud_result": "予算内で",
        "bud_result2": "件のスペースが利用可能です！",

        "prd_header": "📋 プロジェクト情報 (PRD)",
        "prd_sub": "ソウル展示・スペース発見ダッシュボード — プロジェクト紹介",
        "prd_why_t": "❓ Why — プロジェクトの目的",
        "prd_why_b": "人気ランキングではなく、気分・雰囲気・予算に合ったソウルの展示・文化スペースを見つけるためのプロジェクトです。どこに行くか悩む人々にデータビジュアライゼーションによる個人化された推薦を提供します。",
        "prd_who_t": "👥 Who — 対象ユーザー",
        "prd_who_b": ["🧑‍🎨 20代の若者・展示愛好家","💑 デートコースを探すカップル","🌸 感性的な空間に興味がある人","🗺️ ソウルの文化・芸術シーンが気になる方"],
        "prd_what_t": "🛠️ What — 主な機能",
        "prd_what_b": ["🌿 気分ベースの推薦システム","🏘️ エリア比較ツール（聖水、北村、梨泰院、漢南…）","💰 予算ベースの推薦","📊 インタラクティブデータビジュアライゼーション"],
        "prd_how_t": "⚙️ How — 技術スタック",
        "prd_how_b": "PythonとStreamlitライブラリを使用し、展示場所・文化スペース・予算情報を含むキュレーションデータセットを活用しています。",
        "prd_steps_t": "#### 🗓️ 3ステップ開発計画",
        "prd_steps": [
            ("1","🏗️ 基本UI & サンプルデータセット","GitHubリポジトリ作成とStreamlit環境設定。ソウルの展示・文化スペースのサンプルデータセット準備。ホームページとナビゲーションのデザイン。"),
            ("2","🔮 インタラクティブ推薦 & ビジュアライゼーション","気分ベースのフィルター実装。予算・エリア比較機能の追加。Plotlyを使ったチャートの可視化。"),
            ("3","✨ UI改善 & 実データ統合","モダンなデザインテーマの適用。実際の展示・文化スペースデータの追加。レスポンシブ改善とデプロイ完了。"),
        ],
        "prd_val_t": "💃 学術的・創造的価値",
        "prd_val_b": "舞踊専攻として、空間・雰囲気・感情体験の関係への関心を反映したプロジェクトです。展示・文化スペースデータをインタラクティブな推薦システムとして構成することで、主観的な感覚をデータ駆動の文化体験に変換します。🌿",

        "card_free": "🎟️ 無料", "card_paid": "💳 有料",
        "card_free_txt": "🎟️ 無料入場", "card_atm": "雰囲気",
    },
}

MOOD_KEYS = {
    "🇰🇷 한국어": {"🌿 Healing":"Healing","🎨 Aesthetic":"Aesthetic","🕯️ Quiet":"Quiet","✨ Artistic":"Artistic","⛩️ Traditional":"Traditional"},
    "🇨🇳 中文":   {"🌿 治愈":"Healing","🎨 美感":"Aesthetic","🕯️ 静谧":"Quiet","✨ 艺术":"Artistic","⛩️ 传统":"Traditional"},
    "🇺🇸 English":{"🌿 Healing":"Healing","🎨 Aesthetic":"Aesthetic","🕯️ Quiet":"Quiet","✨ Artistic":"Artistic","⛩️ Traditional":"Traditional"},
    "🇯🇵 日本語": {"🌿 ヒーリング":"Healing","🎨 審美的":"Aesthetic","🕯️ 静寂":"Quiet","✨ 芸術的":"Artistic","⛩️ 伝統的":"Traditional"},
}

SPACES = [
    {"name":"Seoul Museum of Art (SeMA)",  "area":"Seongsu",   "moods":["Artistic","Aesthetic","Quiet"],       "price":0,     "atm":4.8,"acc":4.5,"pop":4.7,
     "desc":{"🇰🇷 한국어":"빛으로 가득한 갤러리에서 만나는 현대미술 — 회전 전시가 끊임없이 새로운 경험을 선사해요.",
             "🇨🇳 中文":"在充满光线的画廊欣赏现代艺术 — 轮换展览不断带来新体验。",
             "🇺🇸 English":"Contemporary art in light-filled galleries — rotating exhibitions offer fresh experiences.",
             "🇯🇵 日本語":"光溢れるギャラリーで現代アートを — 企画展が常に新しい体験を提供。"}},
    {"name":"Piknic 피크닉",               "area":"Seongsu",   "moods":["Aesthetic","Healing"],                "price":5000,  "atm":4.6,"acc":4.2,"pop":4.5,
     "desc":{"🇰🇷 한국어":"폐공장을 개조한 복합 문화공간 — 카페, 갤러리, 디자인 숍이 따뜻한 감성으로 어우러져 있어요.",
             "🇨🇳 中文":"改建废弃工厂的综合文化空间 — 咖啡馆、画廊、设计店温馨融合。",
             "🇺🇸 English":"A converted factory complex — café, gallery, and design shop in warm harmony.",
             "🇯🇵 日本語":"廃工場をリノベした複合文化施設 — カフェ、ギャラリー、デザインショップが温かく融合。"}},
    {"name":"d'strict Artspace",           "area":"Seongsu",   "moods":["Artistic","Aesthetic"],               "price":18000, "atm":4.9,"acc":4.0,"pop":4.8,
     "desc":{"🇰🇷 한국어":"LED 미디어 설치와 모션 반응 환경이 어우러진 몰입형 디지털 아트 공간이에요.",
             "🇨🇳 中文":"LED媒体装置与动态感应环境融合的沉浸式数字艺术空间。",
             "🇺🇸 English":"Immersive digital art space with LED installations and motion-reactive environments.",
             "🇯🇵 日本語":"LEDメディアアートとモーションインタラクションが融合した没入型デジタルアート空間。"}},
    {"name":"대림미술관 Daelim Museum",    "area":"Seongsu",   "moods":["Aesthetic","Quiet"],                  "price":5000,  "atm":4.5,"acc":4.3,"pop":4.2,
     "desc":{"🇰🇷 한국어":"생활과 사진을 중심으로 한 아늑한 현대미술관 — 개조된 주택 건물이 매력적이에요.",
             "🇨🇳 中文":"以生活和摄影为主题的温馨现代美术馆 — 改建住宅建筑别具魅力。",
             "🇺🇸 English":"Cozy modern art museum focused on lifestyle and photography in a converted house.",
             "🇯🇵 日本語":"ライフスタイルと写真を軸にした居心地よい現代美術館 — 改築した住宅が魅力的。"}},
    {"name":"북촌한옥마을 Bukchon Hanok",  "area":"Bukchon",   "moods":["Traditional","Healing","Quiet"],      "price":0,     "atm":4.9,"acc":4.0,"pop":4.9,
     "desc":{"🇰🇷 한국어":"전통 한옥이 보존된 골목을 걷다 보면 살아있는 역사 속을 거니는 느낌이 들어요.",
             "🇨🇳 中文":"漫步保存完好的传统韩屋小巷，仿佛穿越活生生的历史。",
             "🇺🇸 English":"Walking preserved hanok alleys feels like stepping through living history.",
             "🇯🇵 日本語":"伝統韓屋の路地を歩くと、生きた歴史の中に佇む感覚を覚えます。"}},
    {"name":"가회민화박물관",              "area":"Bukchon",   "moods":["Traditional","Artistic"],             "price":3000,  "atm":4.4,"acc":3.8,"pop":3.6,
     "desc":{"🇰🇷 한국어":"민화와 무속 유물을 소장한 소규모 사립 박물관 — 조용하고 깊이 있는 전통 예술의 세계.",
             "🇨🇳 中文":"收藏民画和萨满文物的小型私立博物馆 — 安静深邃的传统艺术世界。",
             "🇺🇸 English":"Small private museum of folk paintings and shamanic artifacts — quiet and deeply traditional.",
             "🇯🇵 日本語":"民画とシャーマン遺物を所蔵する小さな私立博物館 — 静かで深い伝統芸術の世界。"}},
    {"name":"아라리오뮤지엄 인스페이스",   "area":"Bukchon",   "moods":["Artistic","Quiet"],                   "price":10000, "atm":4.7,"acc":4.2,"pop":4.1,
     "desc":{"🇰🇷 한국어":"드라마틱한 브루탈리즘 내부가 인상적인 국제 현대미술 갤러리예요.",
             "🇨🇳 中文":"以戏剧性野兽派室内设计著称的国际当代艺术画廊。",
             "🇺🇸 English":"International contemporary art gallery with dramatic brutalist interiors.",
             "🇯🇵 日本語":"ドラマチックなブルータリズムの内装が印象的な国際現代アートギャラリー。"}},
    {"name":"리움미술관 Leeum",            "area":"Hannam",    "moods":["Artistic","Aesthetic","Quiet"],       "price":0,     "atm":4.9,"acc":4.5,"pop":4.6,
     "desc":{"🇰🇷 한국어":"렘 콜하스, 마리오 보타, 장 누벨이 설계한 건물 자체가 예술인 삼성 사립 미술관.",
             "🇨🇳 中文":"由雷姆·库哈斯、马里奥·博塔、让·努维尔设计的三星私立美术馆，建筑本身即是艺术。",
             "🇺🇸 English":"Samsung's private museum designed by Rem Koolhaas, Mario Botta & Jean Nouvel — architecture as art.",
             "🇯🇵 日本語":"レム・コールハース、マリオ・ボッタ、ジャン・ヌーヴェル設計 — 建物自体が芸術のサムスン美術館。"}},
    {"name":"Pace Gallery Seoul",          "area":"Hannam",    "moods":["Artistic","Aesthetic"],               "price":0,     "atm":4.6,"acc":4.4,"pop":4.0,
     "desc":{"🇰🇷 한국어":"한남동의 세련된 모더니즘 공간에 자리한 국제 블루칩 현대미술 갤러리.",
             "🇨🇳 中文":"位于汉南洞精致现代主义空间的国际蓝筹当代艺术画廊。",
             "🇺🇸 English":"International blue-chip contemporary art gallery in a sleek modernist Hannam space.",
             "🇯🇵 日本語":"漢南洞のスタイリッシュなモダニズム空間にある国際的なブルーチップ現代アートギャラリー。"}},
    {"name":"국립현대미술관 MMCA",         "area":"Yongsan",   "moods":["Artistic","Traditional","Quiet"],     "price":4000,  "atm":4.8,"acc":4.6,"pop":4.7,
     "desc":{"🇰🇷 한국어":"한국 근현대미술의 중심 — 아름답게 복원된 역사적 건물에 자리한 국립 미술관.",
             "🇨🇳 中文":"韩国近现代艺术中心 — 坐落于精美修复历史建筑中的国立美术馆。",
             "🇺🇸 English":"Korea's foremost modern & contemporary art museum in a beautifully restored historic building.",
             "🇯🇵 日本語":"韓国近現代美術の中心地 — 美しく修復された歴史的建物にある国立美術館。"}},
    {"name":"경복궁 Gyeongbokgung",        "area":"Bukchon",   "moods":["Traditional","Healing"],              "price":3000,  "atm":4.9,"acc":4.7,"pop":4.9,
     "desc":{"🇰🇷 한국어":"서울 최대의 왕궁 — 드넓은 마당과 전통 건축이 절로 발걸음을 느리게 만들어요.",
             "🇨🇳 中文":"首尔最大的王宫 — 宽阔庭院与传统建筑让人不由自主放慢脚步。",
             "🇺🇸 English":"Seoul's grandest royal palace — vast courtyards and traditional architecture invite slow walking.",
             "🇯🇵 日本語":"ソウル最大の王宮 — 広大な中庭と伝統建築が自然と足を遅くさせます。"}},
    {"name":"별마당 도서관",               "area":"Seongsu",   "moods":["Healing","Quiet","Aesthetic"],        "price":0,     "atm":4.7,"acc":4.6,"pop":4.8,
     "desc":{"🇰🇷 한국어":"수천 권의 책이 가득한 천장 높은 아트리움 — 주변 소음이 사라지고 고요함이 찾아와요.",
             "🇨🇳 中文":"数千册书籍填满的高挑中庭 — 周围的喧嚣消散，宁静悄然降临。",
             "🇺🇸 English":"A soaring atrium of thousands of books — noise fades and quiet takes over.",
             "🇯🇵 日本語":"数千冊の本が並ぶ高天井のアトリウム — 周囲の喧騒が消え、静寂が訪れます。"}},
    {"name":"커먼그라운드 Common Ground",  "area":"Seongsu",   "moods":["Aesthetic","Artistic"],               "price":0,     "atm":4.3,"acc":4.4,"pop":4.5,
     "desc":{"🇰🇷 한국어":"컨테이너로 만든 야외 복합공간 — 어반 아트와 감각적인 패션이 함께해요.",
             "🇨🇳 中文":"集装箱打造的户外综合空间 — 城市艺术与时尚感性完美结合。",
             "🇺🇸 English":"Outdoor complex built from shipping containers — urban art meets stylish fashion.",
             "🇯🇵 日本語":"コンテナで作られたアウトドア複合施設 — アーバンアートとファッションが融合。"}},
    {"name":"이태원 문화원",               "area":"Itaewon",   "moods":["Healing","Artistic"],                 "price":0,     "atm":4.2,"acc":4.3,"pop":3.8,
     "desc":{"🇰🇷 한국어":"순환 전시와 루프탑 테라스가 있는 커뮤니티 아트 허브 — 한적하고 사색적인 공간이에요.",
             "🇨🇳 中文":"拥有轮换展览和屋顶露台的社区艺术中心 — 幽静而富有沉思氛围的空间。",
             "🇺🇸 English":"Community art hub with rotating exhibitions and a rooftop terrace — peaceful and reflective.",
             "🇯🇵 日本語":"企画展とルーフトップテラスのあるコミュニティアートハブ — 静かで内省的な空間。"}},
    {"name":"플래툰 쿤스트할레",           "area":"Itaewon",   "moods":["Artistic","Aesthetic"],               "price":0,     "atm":4.4,"acc":4.1,"pop":4.0,
     "desc":{"🇰🇷 한국어":"28개의 컨테이너로 구성된 엣지 있는 크리에이티브 공간 — 음악, 아트, 문화 이벤트가 열려요.",
             "🇨🇳 中文":"由28个集装箱构成的前卫创意空间 — 举办音乐、艺术和文化活动。",
             "🇺🇸 English":"Edgy creative space of 28 shipping containers — music, art and culture events.",
             "🇯🇵 日本語":"28のコンテナで構成されたエッジィなクリエイティブ空間 — 音楽・アート・文化イベントを開催。"}},
    {"name":"이화 벽화마을",               "area":"Insadong",  "moods":["Healing","Artistic","Quiet"],         "price":0,     "atm":4.5,"acc":3.7,"pop":4.2,
     "desc":{"🇰🇷 한국어":"형형색색 벽화로 가득한 언덕 골목 — 도시의 번잡함을 잊게 해주는 조용한 발견의 공간.",
             "🇨🇳 中文":"色彩斑斓壁画装点的山坡小巷 — 让人忘却都市喧嚣的静谧发现之地。",
             "🇺🇸 English":"Hillside alley filled with colorful murals — a quiet discovery away from city noise.",
             "🇯🇵 日本語":"カラフルな壁画が彩る丘の路地 — 都市の喧騒を忘れる静かな発見の場。"}},
    {"name":"쌈지길 Ssamziegil",           "area":"Insadong",  "moods":["Aesthetic","Artistic"],               "price":0,     "atm":4.3,"acc":4.5,"pop":4.6,
     "desc":{"🇰🇷 한국어":"독립 숍, 갤러리, 열린 마당이 이어지는 복합 공간 — 인사동 예술 씬의 중심이에요.",
             "🇨🇳 中文":"独立小店、画廊、开放庭院相连的综合空间 — 仁寺洞艺术圈的核心。",
             "🇺🇸 English":"Connected indie shops, galleries and open courtyards — the heart of Insadong's art scene.",
             "🇯🇵 日本語":"独立ショップ、ギャラリー、開放的な中庭が続く複合施設 — 仁寺洞アートシーンの中心。"}},
    {"name":"창덕궁 & 후원",               "area":"Bukchon",   "moods":["Traditional","Healing","Quiet"],      "price":8000,  "atm":4.9,"acc":4.2,"pop":4.8,
     "desc":{"🇰🇷 한국어":"유네스코 세계유산 — 숨겨진 비밀 정원(후원)은 한국의 자연과 건축 이상향을 담고 있어요.",
             "🇨🇳 中文":"联合国教科文组织世界遗产 — 隐秘的秘密花园（后苑）蕴含韩国自然与建筑的理想境界。",
             "🇺🇸 English":"UNESCO World Heritage site — the secret rear garden embodies Korea's ideal of nature and architecture.",
             "🇯🇵 日本語":"ユネスコ世界遺産 — 隠された秘密の庭園（後苑）は韓国の自然と建築の理想を体現。"}},
    {"name":"스페이스K 서울",              "area":"Seongsu",   "moods":["Artistic","Quiet","Aesthetic"],       "price":0,     "atm":4.6,"acc":4.1,"pop":3.9,
     "desc":{"🇰🇷 한국어":"코오롱이 후원하는 열린 현대미술 공간 — 크고 넉넉한 전시장이 인상적이에요.",
             "🇨🇳 中文":"由科隆赞助的开放现代艺术空间 — 宽敞的展览厅令人印象深刻。",
             "🇺🇸 English":"Kolon-sponsored open contemporary art space — spacious and generous exhibition halls.",
             "🇯🇵 日本語":"コーロン後援の開かれた現代アート空間 — 広々とした展示ホールが印象的。"}},
    {"name":"갤러리현대",                  "area":"Samcheong", "moods":["Artistic","Aesthetic"],               "price":0,     "atm":4.5,"acc":4.4,"pop":4.1,
     "desc":{"🇰🇷 한국어":"한국과 국제 작가를 대표하는 서울 최고(最古)의 상업 갤러리 중 하나.",
             "🇨🇳 中文":"代表韩国和国际艺术家的首尔历史最悠久的商业画廊之一。",
             "🇺🇸 English":"One of Seoul's oldest commercial galleries representing Korean and international artists.",
             "🇯🇵 日本語":"韓国と国際アーティストを代表するソウル最古の商業ギャラリーのひとつ。"}},
    {"name":"국제갤러리 Kukje Gallery",    "area":"Samcheong", "moods":["Artistic","Quiet"],                   "price":0,     "atm":4.7,"acc":4.3,"pop":4.2,
     "desc":{"🇰🇷 한국어":"아름다운 조경의 복합 건물에 자리한 국제 블루칩 갤러리 — 고요하고 세련된 분위기.",
             "🇨🇳 中文":"坐落于美丽景观综合建筑中的国际蓝筹画廊 — 宁静而精致的氛围。",
             "🇺🇸 English":"Leading international gallery in a beautifully landscaped complex — quiet and refined.",
             "🇯🇵 日本語":"美しい造景の複合ビルに位置する国際的ブルーチップギャラリー — 静かで洗練された雰囲気。"}},
    {"name":"더현대 서울 The Hyundai",     "area":"Yongsan",   "moods":["Aesthetic","Healing"],                "price":0,     "atm":4.6,"acc":4.8,"pop":4.9,
     "desc":{"🇰🇷 한국어":"하늘 정원과 현대미술 설치, 몰입형 팝업 공간이 공존하는 혁신적인 백화점.",
             "🇨🇳 中文":"天空花园、现代艺术装置和沉浸式快闪空间共存的创新百货公司。",
             "🇺🇸 English":"Innovative department store with sky gardens, contemporary art installations and immersive pop-ups.",
             "🇯🇵 日本語":"空中庭園、現代アートインスタレーション、没入型ポップアップが共存する革新的デパート。"}},
    {"name":"서울 밤도깨비 야시장",        "area":"Yongsan",   "moods":["Aesthetic","Healing"],                "price":0,     "atm":4.7,"acc":4.6,"pop":4.8,
     "desc":{"🇰🇷 한국어":"별빛 아래 먹거리·공예품·라이브 공연이 펼쳐지는 계절 야간 마켓.",
             "🇨🇳 中文":"星光下举办的季节性夜市 — 美食、手工艺品和现场演出。",
             "🇺🇸 English":"Seasonal night market under the stars — street food, crafts and live performances.",
             "🇯🇵 日本語":"星空の下で開かれる季節の夜市 — 屋台料理、クラフト、ライブパフォーマンス。"}},
    {"name":"트릭아이뮤지엄",              "area":"Hongdae",   "moods":["Aesthetic","Artistic"],               "price":15000, "atm":4.0,"acc":4.6,"pop":4.5,
     "desc":{"🇰🇷 한국어":"방문자가 그림 속 주인공이 되는 트롱프뢰유 아트 뮤지엄 — 신나고 몸으로 즐기는 공간!",
             "🇨🇳 中文":"让访客成为画中主角的错视艺术博物馆 — 令人兴奋的身体互动体验！",
             "🇺🇸 English":"Trompe-l'oeil art museum where you become part of the paintings — fun and physical!",
             "🇯🇵 日本語":"訪問者が絵の主人公になるトロンプルイユアートミュージアム — 楽しくてフィジカルな体験！"}},
    {"name":"홍대 아트브릿지 팝업",        "area":"Hongdae",   "moods":["Artistic","Aesthetic"],               "price":0,     "atm":4.1,"acc":4.7,"pop":4.3,
     "desc":{"🇰🇷 한국어":"신진 한국 작가를 소개하는 계절 팝업 갤러리 — 홍대 보행자 거리 따라 만나게 돼요.",
             "🇨🇳 中文":"介绍新兴韩国艺术家的季节性快闪画廊 — 沿弘大步行街分布。",
             "🇺🇸 English":"Seasonal pop-up gallery showcasing emerging Korean artists along Hongdae's pedestrian street.",
             "🇯🇵 日本語":"新進韓国アーティストを紹介する季節のポップアップギャラリー — 弘大歩行者道路沿いに点在。"}},
    {"name":"서울사진미술관",              "area":"Itaewon",   "moods":["Quiet","Artistic","Aesthetic"],       "price":6000,  "atm":4.6,"acc":4.2,"pop":3.9,
     "desc":{"🇰🇷 한국어":"다큐멘터리부터 파인 아트까지 — 깊이 있는 사진 아카이브와 순환 전시가 인상적인 공간.",
             "🇨🇳 中文":"从纪录片到纯艺术 — 深度摄影档案和轮换展览令人印象深刻的空间。",
             "🇺🇸 English":"From documentary to fine art photography — deep archives and rotating exhibitions.",
             "🇯🇵 日本語":"ドキュメンタリーからファインアートまで — 深い写真アーカイブと企画展が印象的な空間。"}},
    {"name":"한남더힐 갤러리 워크",        "area":"Hannam",    "moods":["Healing","Aesthetic","Quiet"],        "price":0,     "atm":4.5,"acc":3.8,"pop":4.1,
     "desc":{"🇰🇷 한국어":"한남 주거 단지 사이를 걸으며 만나는 야외 조각 정원 — 차분하고 감각적이에요.",
             "🇨🇳 中文":"漫步汉南住宅区之间邂逅的户外雕塑花园 — 宁静而感性。",
             "🇺🇸 English":"Outdoor sculpture garden through Hannam's residential district — calm and sensory.",
             "🇯🇵 日本語":"漢南住宅地区を歩きながら出会う野外彫刻庭園 — 落ち着いて感性的。"}},
    {"name":"서울공예박물관",              "area":"Bukchon",   "moods":["Traditional","Aesthetic","Quiet"],    "price":0,     "atm":4.6,"acc":4.3,"pop":4.0,
     "desc":{"🇰🇷 한국어":"한국 전통 공예의 아름다움을 재발견하는 박물관 — 잘 복원된 근대 건물 안에 자리해요.",
             "🇨🇳 中文":"重新发现韩国传统工艺之美的博物馆 — 坐落于修缮完好的近代建筑中。",
             "🇺🇸 English":"Museum rediscovering the beauty of Korean traditional crafts in a well-restored modern building.",
             "🇯🇵 日本語":"韓国伝統工芸の美を再発見する博物館 — よく修復された近代建築の中に位置。"}},
]

NEIGHBORHOODS = {
    "Seongsu":   {"vibe":"🏭 Industrial Chic",  "atm":4.5,"acc":4.3,"pop":4.6,"avg_price":3000,
                  "best":{"🇰🇷 한국어":"아트+커피 데이트","🇨🇳 中文":"艺术+咖啡约会","🇺🇸 English":"Art + Coffee Date","🇯🇵 日本語":"アート+カフェデート"},
                  "hex":"#c4714a"},
    "Bukchon":   {"vibe":"⛩️ Historic Calm",    "atm":4.8,"acc":3.9,"pop":4.5,"avg_price":2000,
                  "best":{"🇰🇷 한국어":"전통 문화 탐방","🇨🇳 中文":"传统文化探访","🇺🇸 English":"Traditional Culture Tour","🇯🇵 日本語":"伝統文化散策"},
                  "hex":"#7a9e8e"},
    "Itaewon":   {"vibe":"🌍 Cosmopolitan",      "atm":4.2,"acc":4.5,"pop":4.3,"avg_price":5000,
                  "best":{"🇰🇷 한국어":"국제 아트 씬","🇨🇳 中文":"国际艺术圈","🇺🇸 English":"International Art Scene","🇯🇵 日本語":"国際アートシーン"},
                  "hex":"#b8924a"},
    "Hannam":    {"vibe":"🎨 Refined Luxury",    "atm":4.6,"acc":4.3,"pop":4.4,"avg_price":0,
                  "best":{"🇰🇷 한국어":"갤러리 호핑","🇨🇳 中文":"画廊巡游","🇺🇸 English":"Gallery Hopping","🇯🇵 日本語":"ギャラリーホッピング"},
                  "hex":"#d4856e"},
    "Hongdae":   {"vibe":"🎸 Youthful Energy",   "atm":4.0,"acc":4.7,"pop":4.8,"avg_price":3000,
                  "best":{"🇰🇷 한국어":"인디·스트리트 아트","🇨🇳 中文":"独立街头艺术","🇺🇸 English":"Indie & Street Art","🇯🇵 日本語":"インディー・ストリートアート"},
                  "hex":"#8c78c3"},
    "Insadong":  {"vibe":"🖼️ Artisan Soul",      "atm":4.4,"acc":4.5,"pop":4.6,"avg_price":0,
                  "best":{"🇰🇷 한국어":"공예·문화 체험","🇨🇳 中文":"工艺文化体验","🇺🇸 English":"Craft & Culture","🇯🇵 日本語":"工芸・文化体験"},
                  "hex":"#64a078"},
    "Samcheong": {"vibe":"🌸 Quiet Elegance",    "atm":4.7,"acc":4.2,"pop":4.2,"avg_price":0,
                  "best":{"🇰🇷 한국어":"파인 아트 갤러리","🇨🇳 中文":"纯艺术画廊","🇺🇸 English":"Fine Art Galleries","🇯🇵 日本語":"ファインアートギャラリー"},
                  "hex":"#a082c3"},
    "Yongsan":   {"vibe":"🏛️ Urban Grand",      "atm":4.5,"acc":4.7,"pop":4.6,"avg_price":2000,
                  "best":{"🇰🇷 한국어":"국립 박물관","🇨🇳 中文":"国立博物馆","🇺🇸 English":"National Museums","🇯🇵 日本語":"国立博物館"},
                  "hex":"#c39b64"},
}

MOOD_EMOJI = {"Healing":"🌿","Aesthetic":"🎨","Quiet":"🕯️","Artistic":"✨","Traditional":"⛩️"}

df = pd.DataFrame([{**s, "desc": s["desc"]["🇰🇷 한국어"]} for s in SPACES])
df["free"] = df["price"] == 0

def hex_to_rgba(h, a=0.15):
    h = h.lstrip("#")
    return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"

BG, WH, FC, GC = "#faf7f2", "#ffffff", "#6b5e52", "#ede6d9"
BASE = dict(plot_bgcolor=BG, paper_bgcolor=WH, font=dict(color=FC), margin=dict(t=10,b=10))

# ── SIDEBAR ──
with st.sidebar:
    lang = st.selectbox("🌐", list(T.keys()), label_visibility="collapsed")
    tx = T[lang]
    st.markdown(tx["app_title"])
    st.caption(tx["app_caption"])
    st.markdown("---")
    page = st.radio(tx["page_label"], tx["pages"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"<div style='font-size:12px;color:#a8998a;line-height:1.8'>{tx['sidebar_info']}</div>", unsafe_allow_html=True)

def render_card(s):
    is_free = (s["price"] == 0)
    desc = s["desc"][lang] if isinstance(s["desc"], dict) else s["desc"]
    fb = f'<span class="badge badge-free">{tx["card_free"]}</span>' if is_free else f'<span class="badge badge-paid">{tx["card_paid"]}</span>'
    mb = "".join(f'<span class="badge badge-mood">{MOOD_EMOJI.get(m,"")} {m}</span>' for m in s["moods"])
    pt = tx["card_free_txt"] if is_free else f"💳 ₩{s['price']:,}"
    st.markdown(f"""<div class="place-card">
      <div class="card-title">{s['name']} {fb}</div>
      <div class="card-area">📍 {s['area']}</div>
      <div class="card-desc">{desc}</div>
      <div>{mb}</div>
      <div class="card-price">{pt} &nbsp;·&nbsp; ⭐ {tx['card_atm']} {s['atm']}/5</div>
    </div>""", unsafe_allow_html=True)

# ════════════ OVERVIEW ════════════
if page == tx["pages"][0]:
    st.markdown(f'<div class="sec-header">{tx["ov_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">{tx["ov_sub"]}</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric(tx["ov_m1"], len(df))
    c2.metric(tx["ov_m2"], df["area"].nunique())
    c3.metric(tx["ov_m3"], f"{int(df['free'].mean()*100)}%")
    c4.metric(tx["ov_m4"], f"{df['atm'].mean():.1f}")
    st.markdown("---")
    cl, cr = st.columns(2)
    with cl:
        st.markdown(tx["ov_c1"])
        nbc = df.groupby("area").size().reset_index(name="count")
        fig = px.bar(nbc,x="area",y="count",color="area",
                     color_discrete_map={a:NEIGHBORHOODS[a]["hex"] for a in nbc["area"]},
                     labels={"area":tx["ov_bar_x"],"count":tx["ov_bar_y"]})
        fig.update_layout(**BASE,height=280,showlegend=False)
        fig.update_traces(marker_line_width=0)
        fig.update_xaxes(gridcolor=GC); fig.update_yaxes(gridcolor=GC)
        st.plotly_chart(fig,use_container_width=True)
    with cr:
        st.markdown(tx["ov_c2"])
        am=[m for ms in df["moods"] for m in ms]
        mc=pd.Series(am).value_counts().reset_index(); mc.columns=["mood","count"]
        mc["label"]=mc["mood"].apply(lambda m:f"{MOOD_EMOJI.get(m,'')} {m}")
        fig2=px.pie(mc,names="label",values="count",hole=0.5,
                    color_discrete_sequence=["#7a9e8e","#c4714a","#b8a0d0","#d4856e","#b8924a"])
        fig2.update_layout(**BASE,height=280)
        st.plotly_chart(fig2,use_container_width=True)
    st.markdown(tx["ov_c3"])
    pb=["🎟️ Free","₩1–5k","₩5–10k","₩10–20k","₩20k+"]
    pc=[len(df[df["price"]==0]),len(df[(df["price"]>0)&(df["price"]<=5000)]),
        len(df[(df["price"]>5000)&(df["price"]<=10000)]),len(df[(df["price"]>10000)&(df["price"]<=20000)]),len(df[df["price"]>20000])]
    fig3=px.bar(x=pb,y=pc,color=pb,color_discrete_sequence=["#7a9e8e","#b8924a","#c4714a","#d4856e","#b8a0c8"],
                labels={"x":tx["ov_price_x"],"y":tx["ov_bar_y"]})
    fig3.update_layout(**BASE,height=260,showlegend=False)
    fig3.update_traces(marker_line_width=0)
    fig3.update_xaxes(gridcolor=GC); fig3.update_yaxes(gridcolor=GC)
    st.plotly_chart(fig3,use_container_width=True)

# ════════════ MOOD FINDER ════════════
elif page == tx["pages"][1]:
    st.markdown(f'<div class="sec-header">{tx["mood_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">{tx["mood_sub"]}</div>', unsafe_allow_html=True)
    st.info(tx["mood_info"], icon="💃")
    sel = st.multiselect(tx["mood_select"], tx["mood_opts"], default=[tx["mood_opts"][0]])
    mk = MOOD_KEYS[lang]
    keys = [mk[s] for s in sel if s in mk]
    fil = [s for s in SPACES if any(m in s["moods"] for m in keys)]
    if not fil:
        st.warning(tx["mood_none"])
    else:
        st.success(f"✅ **{len(fil)}** {tx['mood_found']}")
        c1,c2=st.columns(2)
        for i,s in enumerate(fil):
            with (c1 if i%2==0 else c2): render_card(s)

# ════════════ NEIGHBORHOODS ════════════
elif page == tx["pages"][2]:
    st.markdown(f'<div class="sec-header">{tx["nb_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">{tx["nb_sub"]}</div>', unsafe_allow_html=True)
    sel_nbs=st.multiselect(tx["nb_select"],list(NEIGHBORHOODS.keys()),default=["Seongsu","Bukchon","Itaewon","Hannam"])
    if len(sel_nbs)<2:
        st.warning(tx["nb_warn"])
    else:
        cl,cr=st.columns(2)
        with cl:
            st.markdown(tx["nb_radar"])
            fig_r=go.Figure()
            for nb in sel_nbs:
                d=NEIGHBORHOODS[nb]
                fig_r.add_trace(go.Scatterpolar(r=[d["atm"],d["acc"],d["pop"]],
                    theta=["Atmosphere","Accessibility","Popularity"],fill="toself",name=nb,
                    line_color=d["hex"],fillcolor=hex_to_rgba(d["hex"],0.12)))
            fig_r.update_layout(polar=dict(bgcolor=BG,
                radialaxis=dict(visible=True,range=[3.5,5],gridcolor=GC,tickfont=dict(color="#a8998a")),
                angularaxis=dict(gridcolor=GC,tickfont=dict(color=FC))),
                paper_bgcolor=WH,font=dict(color=FC),legend=dict(font=dict(color=FC)),
                margin=dict(t=20,b=20),height=340)
            st.plotly_chart(fig_r,use_container_width=True)
        with cr:
            st.markdown(tx["nb_scatter"])
            fig_s=go.Figure()
            for nb in sel_nbs:
                d=NEIGHBORHOODS[nb]
                fig_s.add_trace(go.Scatter(x=[d["acc"]],y=[d["pop"]],mode="markers+text",
                    name=nb,text=[nb],textposition="top center",
                    marker=dict(size=18,color=d["hex"],line=dict(width=2,color="#fff"))))
            fig_s.update_layout(**BASE,xaxis=dict(title="Accessibility",range=[3.4,5.1],gridcolor=GC),
                yaxis=dict(title="Popularity",range=[3.4,5.1],gridcolor=GC),showlegend=False,height=340)
            st.plotly_chart(fig_s,use_container_width=True)
        st.markdown(tx["nb_table"])
        cols=tx["nb_cols"]
        rows=[{cols[0]:nb, cols[1]:NEIGHBORHOODS[nb]["vibe"],
               cols[2]:NEIGHBORHOODS[nb]["atm"], cols[3]:NEIGHBORHOODS[nb]["acc"],
               cols[4]:NEIGHBORHOODS[nb]["pop"],
               cols[5]:tx["nb_free"] if NEIGHBORHOODS[nb]["avg_price"]==0 else f"₩{NEIGHBORHOODS[nb]['avg_price']:,}",
               cols[6]:NEIGHBORHOODS[nb]["best"][lang]} for nb in sel_nbs]
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        st.markdown(tx["nb_cards"])
        nb_sp=[s for s in SPACES if s["area"] in sel_nbs]
        c1,c2=st.columns(2)
        for i,s in enumerate(nb_sp):
            with (c1 if i%2==0 else c2): render_card(s)

# ════════════ BUDGET ════════════
elif page == tx["pages"][3]:
    st.markdown(f'<div class="sec-header">{tx["bud_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">{tx["bud_sub"]}</div>', unsafe_allow_html=True)
    cs,cm=st.columns([2,1])
    with cs: budget=st.slider(tx["bud_slider"],0,30000,15000,step=1000,format="₩%d")
    with cm: mf=st.selectbox(tx["bud_mood"],[tx["bud_all"]]+tx["mood_opts"])
    mk=MOOD_KEYS[lang]
    mood_key=None if mf==tx["bud_all"] else mk.get(mf)
    fil=[s for s in SPACES if s["price"]<=budget and (mood_key is None or mood_key in s["moods"])]
    cl,cr=st.columns(2)
    with cl:
        st.markdown(tx["bud_line"])
        ths=[0,3000,5000,8000,10000,15000,20000,30000]
        lth=["Free" if t==0 else f"₩{t:,}" for t in ths]
        cth=[len([s for s in SPACES if s["price"]<=t]) for t in ths]
        fig_l=px.line(x=lth,y=cth,markers=True,color_discrete_sequence=["#c4714a"],
                      labels={"x":tx["bud_line_x"],"y":tx["bud_line_y"]})
        fig_l.update_traces(line_width=2.5,marker_size=8)
        fig_l.update_layout(**BASE,height=260)
        fig_l.update_xaxes(gridcolor=GC); fig_l.update_yaxes(gridcolor=GC)
        st.plotly_chart(fig_l,use_container_width=True)
    with cr:
        st.markdown(tx["bud_bar"])
        tl=["🎟️ Free","~₩5k","₩5–10k","₩10k+"]
        tc=[len(df[df["price"]==0]),len(df[(df["price"]>0)&(df["price"]<=5000)]),
            len(df[(df["price"]>5000)&(df["price"]<=10000)]),len(df[df["price"]>10000])]
        fig_t=px.bar(x=tl,y=tc,color=tl,color_discrete_sequence=["#7a9e8e","#b8924a","#c4714a","#d4856e"],
                     labels={"x":tx["bud_line_x"],"y":tx["bud_line_y"]})
        fig_t.update_layout(**BASE,height=260,showlegend=False)
        fig_t.update_traces(marker_line_width=0)
        fig_t.update_xaxes(gridcolor=GC); fig_t.update_yaxes(gridcolor=GC)
        st.plotly_chart(fig_t,use_container_width=True)
    lbl=tx["bud_free_only"] if budget==0 else f"₩{budget:,}"
    st.success(f"✅ **{lbl}** {tx['bud_result']} **{len(fil)}** {tx['bud_result2']}")
    c1,c2=st.columns(2)
    for i,s in enumerate(sorted(fil,key=lambda x:x["price"])):
        with (c1 if i%2==0 else c2): render_card(s)

# ════════════ PROJECT INFO ════════════
elif page == tx["pages"][4]:
    st.markdown(f'<div class="sec-header">{tx["prd_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-sub">{tx["prd_sub"]}</div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        items="".join(f"<li>{i}</li>" for i in tx["prd_who_b"])
        st.markdown(f'<div class="prd-card"><h4>{tx["prd_why_t"]}</h4><p>{tx["prd_why_b"]}</p></div>',unsafe_allow_html=True)
    with c2:
        items="".join(f"<li>{i}</li>" for i in tx["prd_who_b"])
        st.markdown(f'<div class="prd-card"><h4>{tx["prd_who_t"]}</h4><ul>{items}</ul></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c3,c4=st.columns(2)
    with c3:
        items="".join(f"<li>{i}</li>" for i in tx["prd_what_b"])
        st.markdown(f'<div class="prd-card"><h4>{tx["prd_what_t"]}</h4><ul>{items}</ul></div>',unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="prd-card"><h4>{tx["prd_how_t"]}</h4><p><span class="tech-pill">Python 3.9+</span><span class="tech-pill">Streamlit</span><span class="tech-pill">Pandas</span><span class="tech-pill">Plotly</span><span class="tech-pill">GitHub</span><span class="tech-pill">Streamlit Cloud</span></p><p style="margin-top:12px">{tx["prd_how_b"]}</p></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown(tx["prd_steps_t"])
    for num,title,desc in tx["prd_steps"]:
        st.markdown(f'<div class="step-card"><span class="step-num">{num}</span><div><strong>{title}</strong><br><span style="font-size:13px;color:#6b5e52">{desc}</span></div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown(f'<div class="prd-card"><h4>{tx["prd_val_t"]}</h4><p>{tx["prd_val_b"]}</p></div>',unsafe_allow_html=True)
