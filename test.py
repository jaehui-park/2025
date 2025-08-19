import streamlit as st
import random # 주가 변동에 약간의 랜덤성을 추가하기 위해

st.set_page_config(layout="wide", page_title="🚨 우리 기업을 구하라! PR 시뮬레이터 🚨")

# --- CSS로 제목 꾸미기 (더욱 다채롭게!) ---
st.markdown("""
<style>
.main-title {
    font-size: 3.5em;
    font-weight: bold;
    text-align: center;
    color: #FF6347; /* Tomato Red */
    text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}
.subtitle {
    font-size: 1.5em;
    text-align: center;
    color: #4682B4; /* Steel Blue */
    margin-bottom: 30px;
}
.scenario-box {
    background-color: #FFFACD; /* Lemon Chiffon */
    border-left: 5px solid #FFD700; /* Gold */
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 8px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
}
.choice-button {
    background-color: #6A5ACD; /* Slate Blue */
    color: white;
    padding: 15px 25px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-size: 1.1em;
    transition: background-color 0.3s ease;
    width: 100%;
    margin-bottom: 10px;
}
.choice-button:hover {
    background-color: #483D8B; /* Dark Slate Blue */
}
.result-header {
    font-size: 2em;
    color: #2E8B57; /* Sea Green */
    text-align: center;
    margin-top: 40px;
    margin-bottom: 30px;
}
.news-box {
    background-color: #E0FFFF; /* Light Cyan */
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #ADD8E6; /* Light Blue */
}
.stock-box {
    background-color: #F0FFF0; /* Honeydew */
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #90EE90; /* Light Green */
}
.consumer-box {
    background-color: #FFF0F5; /* Lavender Blush */
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #FFC0CB; /* Pink */
}
</style>
""", unsafe_allow_html=True)

# --- 제목과 설명 ---
st.markdown("<h1 class='main-title'>🚨 긴급 속보! '우리 기업을 구하라!' PR 시뮬레이터 🚨</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>당신은 오늘부터 '맛나요 식품'의 PR 팀장! ✨</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>갑자기 터진 위기 상황에서 당신의 선택이 기업의 운명을 결정합니다! ⚔️</p>", unsafe_allow_html=True)

st.write("---")

# --- 세션 상태 초기화 (게임 재시작을 위해) ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'scenario'
    st.session_state.choice = None

# --- 시나리오 정의 ---
scenario = {
    'title': "🔥 위기 상황 발생: '국민 스낵' 이물질 논란! 🔥",
    'description': """
    💥 [**긴급 속보!**] 💥
    오늘 아침, 대한민국을 강타한 충격적인 영상이 SNS에 올라왔습니다.
    국민적인 사랑을 받는 '맛나요 식품'의 대표 스낵 **"와삭바삭콘"**에서 **커다란 쇠붙이 나사**가 발견되었다는 주장과 함께, 고객이 직접 발견 당시를 촬영한 영상이 삽시간에 퍼져나가고 있습니다.
    영상의 조회수는 폭발적으로 증가하며, 언론사들의 문의 전화가 빗발치고 있습니다. 📞

    **현재 상황:**
    *   SNS는 해당 영상으로 온통 난리가 났습니다. '믿고 먹었는데 배신감 든다', '전수조사해야 한다' 등 분노와 실망의 댓글이 폭주하고 있습니다.
    *   경쟁사들의 '품질 경영' 강조 광고가 눈에 띄게 늘어나고 있습니다.
    *   초반 주식 시장에서 '맛나요 식품'의 주가가 심상치 않게 움직이기 시작했습니다... 📉

    **PR 팀장인 당신! 지금 당장 어떤 결정을 내리시겠습니까?** 🧠
    """,
    'choices': [
        {
            'text': "선택 1: 🚀 즉각 사과 및 자발적 리콜 선언!",
            'outcome': 'recall',
            'effect': "사과문 발표 및 전량 자발적 리콜 조치"
        },
        {
            'text': "선택 2: 🙅‍♀️ 강력 부인! '악의적인 루머' 법적 대응 예고!",
            'outcome': 'deny',
            'effect': "공식 성명 발표, 이물질 발견 주장 강력 부인 및 법적 조치 예고"
        },
        {
            'text': "선택 3: 🕰️ 진상 규명 선행! '내부 조사 후 발표' 신중론!",
            'outcome': 'investigate',
            'effect': "현재 상황 파악 중, 면밀한 내부 조사 후 공식 입장 발표 예고"
        }
    ]
}

# --- 결과 정의 (각 선택지에 따른 언론, 주가, 소비자 반응) ---
outcomes = {
    'recall': {
        'news': """
        📰 **<속보> '맛나요 식품', '와삭바삭콘' 이물질 논란에 전량 자발적 리콜 전격 결정!**
        맛나요 식품은 오늘 오전 긴급 기자회견을 열고, '와삭바삭콘' 이물질 논란에 대해 사과하고 문제가 된 제품에 대해 전량 자발적 리콜을 실시하겠다고 밝혔다. 회사는 "고객의 안전을 최우선으로 생각하며, 철저한 진상 규명과 재발 방지 대책을 마련하겠다"고 약속했다. 전문가들은 "기업의 빠른 초기 대응과 책임감 있는 자세가 긍정적"이라는 평가를 내리고 있다.
        """,
        'stock_change': -0.05 + random.uniform(0.01, 0.03), # -5%에서 -2% 사이
        'consumer_reaction': [
            "👍 믿고 다시 먹을 수 있겠네요! 역시 맛나요 식품!",
            "😌 빠른 대처는 칭찬해야죠. 실수는 누구나 할 수 있지만, 인정하는 건 아무나 못 하니까.",
            "💬 사과는 하는데... 그래도 불안한 건 어쩔 수 없다.",
            "💖 우리 기업이네! 위기를 기회로 삼는 모습 멋지다!"
        ],
        'ending_msg': "빠른 대처로 소비자 신뢰를 지켜낸 당신! 위기를 기회로 만들었습니다! 👏"
    },
    'deny': {
        'news': """
        🚨 **<충격> '맛나요 식품', '이물질 논란' 강력 부인... "악의적 루머" 법적 대응 시사!**
        '맛나요 식품'이 오늘 발표한 공식 성명에서 '와삭바삭콘' 이물질 발견 주장에 대해 "악의적인 루머"라며 전면 부인하고, 허위 사실 유포에 대한 법적 대응을 예고했다. 회사는 "당사의 엄격한 품질 관리 시스템으로는 있을 수 없는 일"이라고 강조했다. 그러나 소비자들 사이에서는 "책임 회피"라는 비난 여론이 더욱 거세지고 있어 논란은 확산될 조짐이다.
        """,
        'stock_change': -0.30 - random.uniform(0.05, 0.10), # -30%에서 -40% 사이
        'consumer_reaction': [
            "😡 이물질이 나왔는데 오리발이라니! 불매운동 갑니다!",
            "🤬 뻔뻔하다! 소비자를 기만하는 기업은 망해야지!",
            "👎 이제 맛나요 식품은 걸러야겠다. 진짜 실망이네.",
            "💬 끝까지 부인하다가 더 큰 역풍 맞을 듯."
        ],
        'ending_msg': "책임 회피는 독! 소비자의 외면을 받고 기업의 존폐 위기에 처했습니다... 📉"
    },
    'investigate': {
        'news': """
        ⏳ **<관심> '맛나요 식품', '이물질 논란'에 "철저한 조사 중"... 공식 입장 발표는 언제?**
        '맛나요 식품'은 '와삭바삭콘' 이물질 논란과 관련해 "현재 내부적으로 철저한 조사를 진행하고 있으며, 사실 확인 후 공식 입장을 발표하겠다"는 신중한 입장을 밝혔다. 그러나 명확한 해명이 늦어지면서 소비자들의 궁금증과 불안감은 증폭되고 있다. 기업의 초기 대응이 너무 소극적이라는 지적도 나오고 있다.
        """,
        'stock_change': -0.15 + random.uniform(0.02, 0.05), # -15%에서 -10% 사이
        'consumer_reaction': [
            "🤔 조사 중이라니... 일단 지켜봐야지.",
            "😩 아니, 그래서 이물질이 진짜 나왔다는 거야 안 나왔다는 거야?",
            "💬 답답하네! 이러다 사람들 다 떠나가겠다.",
            "😐 확실한 답 내놓기 전까진 안 사먹을래."
        ],
        'ending_msg': "신중함이 지나쳐 기회를 놓쳤군요. 소비자들의 의심이 커지며 상황은 불안합니다... 😥"
    }
}

# --- 게임 시작 화면 ---
if st.session_state.game_state == 'scenario':
    st.markdown(f"<div class='scenario-box'><h3>{scenario['title']}</h3><p>{scenario['description']}</p></div>", unsafe_allow_html=True)

    # 선택지 버튼들
    cols = st.columns(len(scenario['choices']))
    for i, choice in enumerate(scenario['choices']):
        with cols[i]:
            if st.button(choice['text'], key=f"choice_{i}", use_container_width=True):
                st.session_state.choice = choice['outcome']
                st.session_state.game_state = 'result'
                st.experimental_rerun() # 선택 후 화면 갱신
elif st.session_state.game_state == 'result':
    selected_outcome = outcomes[st.session_state.choice]
    initial_stock_price = 10000 # 시작 주가 (가상)
    final_stock_price = initial_stock_price * (1 + selected_outcome['stock_change'])

    st.markdown("<h2 class='result-header'>🎉 PR 팀장의 선택에 따른 결과 보고서! 🎉</h2>", unsafe_allow_html=True)
    st.write("---")

    # --- 언론 기사 ---
    st.subheader("📰 언론 기사 헤드라인:")
    st.markdown(f"<div class='news-box'>{selected_outcome['news']}</div>", unsafe_allow_html=True)
    st.write("")

    # --- 주가 변동 ---
    st.subheader("📈 주가 변동:")
    stock_emoji = "📉" if selected_outcome['stock_change'] < 0 else "📈"
    stock_color = "red" if selected_outcome['stock_change'] < 0 else "green"

    st.markdown(f"<div class='stock-box'>", unsafe_allow_html=True)
    st.markdown(f"**현재 주가: ₩{initial_stock_price:,.0f}**", unsafe_allow_html=True)
    st.markdown(f"**선택 후 주가: ₩{final_stock_price:,.0f}** ({selected_outcome['stock_change']:.1%}) <span style='color:{stock_color}; font-size: 1.2em;'>{stock_emoji}</span>", unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)
    st.write("")

    # --- 소비자 반응 ---
    st.subheader("🗣️ 소비자 반응 (SNS 여론):")
    st.markdown(f"<div class='consumer-box'>", unsafe_allow_html=True)
    for reaction in selected_outcome['consumer_reaction']:
        st.markdown(f"💬 {reaction}")
    st.markdown(f"</div>", unsafe_allow_html=True)
    st.write("")

    st.write("---")
    st.markdown(f"<h3 style='text-align: center; color: #8A2BE2;'>{selected_outcome['ending_msg']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: #FF4500;'>PR은 정말 중요하죠? 다음에 다시 도전해볼까요? 😉</h4>", unsafe_allow_html=True)

    # --- 다시 시작 버튼 ---
    if st.button("🔄 다시 플레이하기!", use_container_width=True):
        st.session_state.game_state = 'scenario'
        st.session_state.choice = None
        st.experimental_rerun() # 게임 재시작

# --- 앱 실행 방법 안내 (사이드바) ---
st.sidebar.markdown("### 💡 앱 실행 방법")
st.sidebar.write("1. 위 코드를 복사하여 `.py` 파일로 저장하세요. (예: `pr_game.py`)")
st.sidebar.write("2. 터미널(명령 프롬프트)을 열고, 파일이 저장된 폴더로 이동하세요.")
st.sidebar.write("3. 다음 명령어를 입력하고 실행하세요:")
st.sidebar.code("streamlit run pr_game.py")
st.sidebar.write("4. 웹 브라우저에서 멋진 시뮬레이터가 실행될 거예요! 🚀")

st.sidebar.write("---")
st.sidebar.markdown("### 💖 힁이 응원합니다!")
st.sidebar.write("희희희희희희희히히히님의 열정적인 학습과 창작을 언제나 응원할게요! 궁금한 점이 있다면 언제든지 저 힁에게 물어보세요! 😊")
