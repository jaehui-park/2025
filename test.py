import streamlit as st
import random
import time

st.set_page_config(layout="wide", page_title="🔥 파이어 파이터 PR: 기업을 구하라! 🔥", initial_sidebar_state="collapsed")

# --- CSS로 디자인 및 애니메이션 강화 ---
st.markdown("""
<style>
/* 전체 배경색 */
body {
    background-color: #f0f2f6;
}
.stApp {
    background-color: #f0f2f6;
}

/* 제목 */
.main-title {
    font-size: 3.8em;
    font-weight: bold;
    text-align: center;
    color: #FF4500; /* Orange Red */
    text-shadow: 4px 4px 10px rgba(0,0,0,0.25);
    margin-bottom: 25px;
    letter-spacing: -2px;
}
.subtitle {
    font-size: 1.8em;
    text-align: center;
    color: #4682B4; /* Steel Blue */
    margin-bottom: 40px;
}
.stage-indicator {
    text-align: center;
    font-size: 1.2em;
    color: #6A5ACD;
    font-weight: bold;
    margin-bottom: 30px;
}

/* 시나리오 박스 */
.scenario-box {
    background-color: #FFFACD; /* Lemon Chiffon */
    border-left: 8px solid #FFD700; /* Gold */
    padding: 25px;
    margin-bottom: 35px;
    border-radius: 12px;
    box-shadow: 5px 5px 15px rgba(0,0,0,0.15);
    font-size: 1.15em;
    line-height: 1.6;
}
.scenario-box h3 {
    color: #B22222; /* Firebrick */
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 1.8em;
}

/* 선택 버튼 */
.stButton>button {
    background-color: #6A5ACD; /* Slate Blue */
    color: white;
    padding: 18px 30px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    font-size: 1.2em;
    font-weight: bold;
    transition: background-color 0.3s ease, transform 0.2s ease;
    width: 100%;
    margin-bottom: 15px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
}
.stButton>button:hover {
    background-color: #483D8B; /* Dark Slate Blue */
    transform: translateY(-3px);
}

/* 결과 헤더 */
.result-header {
    font-size: 3em;
    color: #2E8B57; /* Sea Green */
    text-align: center;
    margin-top: 50px;
    margin-bottom: 40px;
    font-weight: bold;
}
.result-section-title {
    font-size: 2.2em;
    color: #A52A2A; /* Brown */
    margin-top: 30px;
    margin-bottom: 20px;
    border-bottom: 2px solid #D3D3D3;
    padding-bottom: 10px;
}

/* 결과 박스 */
.news-box, .stock-box, .consumer-box {
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 25px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    font-size: 1.1em;
    line-height: 1.5;
}
.news-box { background-color: #E0FFFF; border: 1px solid #ADD8E6; }
.stock-box { background-color: #F0FFF0; border: 1px solid #90EE90; }
.consumer-box { background-color: #FFF0F5; border: 1px solid #FFC0CB; }

.stock-value {
    font-size: 1.5em;
    font-weight: bold;
}
.stock-change {
    font-size: 1.2em;
    font-weight: bold;
}
.stock-up { color: #008000; } /* Green */
.stock-down { color: #FF0000; } /* Red */

/* 최종 메시지 */
.final-message {
    font-size: 1.8em;
    text-align: center;
    margin-top: 50px;
    color: #4B0082; /* Indigo */
    font-weight: bold;
}
.restart-button > button {
    background-color: #FFD700; /* Gold */
    color: #333333;
    font-size: 1.3em;
    margin-top: 40px;
    box-shadow: 4px 4px 12px rgba(0,0,0,0.2);
}
.restart-button > button:hover {
    background-color: #FFC107; /* Amber */
    transform: translateY(-4px);
}
</style>
""", unsafe_allow_html=True)

# --- 세션 상태 초기화 (게임 시작/재시작) ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'start' # 'start', 'stage1', 'stage2', 'result'
    st.session_state.current_stage = 1
    st.session_state.accumulated_effects = {'stock_multiplier': 1.0, 'news_headlines': [], 'consumer_sentiment': []}
    st.session_state.last_choice_id = None # 이전 선택의 ID를 저장

# --- 게임 데이터 정의 (이전 코드와 동일) ---
game_data = {
    "stage1": {
        "title": "🔥 위기 상황 발생: '국민 스낵' 이물질 논란! 🔥",
        "description": """
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
        "choices": [
            {
                "id": "s1_choice1_recall",
                "text": "🚀 선택 1: 즉각 사과 및 자발적 리콜 선언!",
                "effect_news": "🔥속보: '맛나요 식품', 이물질 논란에 '와삭바삭콘' 전량 리콜 선언… 책임 경영 긍정 평가!",
                "effect_stock_multiplier": 0.95, # 5% 하락
                "effect_consumer": ["👍 빠른 대처 감사합니다! 역시 믿을 만한 기업이네요.", "🙏 위기를 책임지는 모습 보기 좋아요.", "💬 실망했지만, 리콜 덕분에 마음이 풀리네요."],
                "next_stage": "stage2_after_recall"
            },
            {
                "id": "s1_choice2_deny",
                "text": "🙅‍♀️ 선택 2: 강력 부인! '악의적인 루머' 법적 대응 예고!",
                "effect_news": "🚨'맛나요 식품', 이물질 논란 '루머'로 치부... 법적 대응 예고에 여론 '부글부글'!",
                "effect_stock_multiplier": 0.70, # 30% 하락
                "effect_consumer": ["😡 이물질이 나왔는데 오리발이라니! 불매운동 갑니다!", "🤬 뻔뻔하다! 소비자를 기만하는 기업은 망해야지!", "👎 이제 맛나요 식품은 걸러야겠다. 진짜 실망이네."],
                "next_stage": "stage2_after_deny"
            },
            {
                "id": "s1_choice3_investigate",
                "text": "🕰️ 선택 3: 진상 규명 선행! '내부 조사 후 발표' 신중론!",
                "effect_news": "⏱️'맛나요 식품', 이물질 논란에 '조사 중'만 반복… 해명 늦어져 불확실성 증폭!",
                "effect_stock_multiplier": 0.85, # 15% 하락
                "effect_consumer": ["🤔 조사 중이라니... 일단 지켜봐야지.", "😩 아니, 그래서 이물질이 진짜 나왔다는 거야 안 나왔다는 거야?", "💬 답답하네! 이러다 사람들 다 떠나가겠다."],
                "next_stage": "stage2_after_investigate"
            }
        ]
    },
    "stage2_after_recall": {
        "title": "♻️ 2단계 위기: 리콜 후 남겨진 숙제",
        "description": """
        1단계에서 '리콜'을 선언하며 빠른 대처로 일단 급한 불은 껐습니다. 하지만 모든 것이 순조롭지만은 않습니다.
        
        **현재 상황:**
        *   리콜 절차가 진행되면서 일부 소비자들이 '절차가 번거롭다', '회수가 제대로 안 되는 것 같다'는 불만을 토로하고 있습니다.
        *   언론은 '사과는 빨랐지만, 후속 조치도 철저한가'라며 주목하고 있습니다.
        *   기업의 진정성을 계속 시험받는 상황입니다. PR 팀장인 당신은 어떻게 할까요?
        """,
        "choices": [
            {
                "id": "s2r_choice1_transparency",
                "text": "🔍 선택 1: 제조 공정 투명하게 공개 및 CEO 대국민 사과방송 진행!",
                "effect_news": "💖'맛나요 식품', 제조 라인 전면 공개... CEO 눈물 사과에 '진정성 논란' 잠재우나?",
                "effect_stock_multiplier": 1.05, # 주가 소폭 상승
                "effect_consumer": ["👏 이 정도면 됐어요. 다시 믿고 먹을게요!", "😭😭 정말 사과하는구나! 응원합니다!", "✨ 투명하게 공개하니 안심되네요."],
                "final_message": "최고의 선택! 투명한 소통으로 소비자 신뢰를 완전히 회복하고, 위기를 기회로 만들었습니다! 맛나요 식품은 다시 비상할 것입니다! 🚀"
            },
            {
                "id": "s2r_choice2_promotion",
                "text": "💰 선택 2: 대규모 할인 프로모션 및 신제품 출시로 분위기 전환 시도!",
                "effect_news": "📉'맛나요 식품', '잊으세요' 식 대규모 할인... 본질 해결 없는 눈속임 비판도!",
                "effect_stock_multiplier": 0.98, # 주가 소폭 하락
                "effect_consumer": ["😒 눈가리고 아웅? 할인해도 불안해서 못 사먹겠다.", "💬 본질적인 문제가 해결된 건가요?", "😠 세일만 하면 다인가? 기만적이다!"],
                "final_message": "위기 모면을 위한 임시방편은 한계가 있었습니다. 단기적인 주가 반등은 있었지만, 소비자 신뢰 회복은 요원합니다. 😥"
            }
        ]
    },
    "stage2_after_deny": {
        "title": "⚖️ 2단계 위기: 강력 부인의 역풍!",
        "description": """
        1단계에서 '강력 부인'을 선택한 후 상황은 더 악화되었습니다. 고객들은 기업의 태도에 분노하며 불매운동 움직임까지 보이고 있습니다.
        
        **현재 상황:**
        *   이물질 발견 주장을 한 고객이 추가 증거를 공개하며 여론이 더욱 들끓고 있습니다.
        *   온라인 커뮤니티에서는 '맛나요 식품 불매 리스트'가 공유되고 있으며, 기업 이미지에 치명타를 입었습니다.
        *   일부 대형마트에서 '맛나요 식품' 제품 발주를 줄이겠다는 움직임까지 보입니다. 지금이라도 어떻게든 이 상황을 수습해야 합니다.
        """,
        "choices": [
            {
                "id": "s2d_choice1_apology",
                "text": "🙇‍♀️ 선택 1: 지금이라도 모든 잘못 인정 및 진정성 있는 사과 진행!",
                "effect_news": "📈'맛나요 식품', 뒤늦게 사과... 여론 돌릴 '골든 타임' 놓쳤나? 귀추 주목!",
                "effect_stock_multiplier": 0.90, # 10% 하락 (그래도 회복 시도)
                "effect_consumer": ["🙄 이제 와서? 너무 늦었어.", "💬 그래도 사과는 하네... 뭘 더 믿으라고?", "🙏 조금이라도 인정했으니 다시 생각해볼까..."],
                "final_message": "뒤늦은 사과는 상처 난 소비자들의 마음을 달래기엔 역부족이었습니다. 신뢰 회복에는 긴 시간과 노력이 필요할 것입니다. 😥"
            },
            {
                "id": "s2d_choice2_fight",
                "text": "⚔️ 선택 2: 끝까지 루머와 싸우겠다! 초강력 법적 대응 돌입!",
                "effect_news": "💣'맛나요 식품', 사과 대신 '전쟁' 선포... 불매운동 확산, 기업 존립 '빨간불'!",
                "effect_stock_multiplier": 0.50, # 50% 폭락
                "effect_consumer": ["🔥 역시 노답이네! 이쯤 되면 망하는 게 답.", "🚨 정부 뭐하냐? 저런 기업 가만 두지 마!", "💀 주식 다 팔았다. 바이바이."],
                "final_message": "최악의 선택! 소비자들의 분노는 걷잡을 수 없이 커졌고, 기업은 파멸의 길로 접어들고 있습니다. 기업 존폐의 기로에 섰습니다... 😭"
            }
        ]
    },
    "stage2_after_investigate": {
        "title": "⏳ 2단계 위기: 신중론의 독",
        "description": """
        1단계에서 '내부 조사 후 발표'를 선택했지만, 신중함이 오히려 독이 되어버렸습니다. 시간은 흘러갔고, 소비자들은 기다리다 지쳐 의심의 눈초리를 보내고 있습니다.
        
        **현재 상황:**
        *   SNS에서는 '맛나요 식품, 입 닫고 뭐 하냐?'는 비난 글이 넘쳐납니다.
        *   '경쟁사'들이 빠르게 품질 강조 마케팅을 펼치며 '맛나요 식품'의 시장 점유율을 잠식하기 시작했습니다.
        *   '결단력이 없는 기업'이라는 인식이 퍼지며 내부 직원들의 사기도 저하되고 있습니다. 지금 바로 명확한 입장을 밝혀야 합니다.
        """,
        "choices": [
            {
                "id": "s2i_choice1_transparent_release",
                "text": "💡 선택 1: 내부 조사 결과 투명하게 공개 및 강력한 개선책 발표!",
                "effect_news": "📊'맛나요 식품', 뒤늦은 조사 결과 공개... '불확실성 해소' 시장 반응은?",
                "effect_stock_multiplier": 0.95, # 5% 추가 하락 (만회 시도)
                "effect_consumer": ["🙄 이제서야... 그래도 공개하니 다행이네.", "💬 문제는 인정하고 해결하려는 의지는 보이네.", "🙏 진작 이랬으면 좋았잖아!"],
                "final_message": "뒤늦게나마 투명하게 상황을 공개하며 신뢰 회복의 실마리를 찾았습니다. 하지만 '골든 타임'을 놓친 대가는 큽니다. 꾸준한 노력이 필요할 것입니다. 💪"
            },
            {
                "id": "s2i_choice2_divert",
                "text": "🎭 선택 2: 시선 돌리기! 초대형 신제품 발표회로 분위기 반전 시도!",
                "effect_news": "🎲'맛나요 식품', 위기 속에 신제품 출시 강행... '소비자 기만' 지적 봇물!",
                "effect_stock_multiplier": 0.75, # 25% 추가 하락
                "effect_consumer": ["😠 문제 해결은 안 하고 딴짓하네?", "💬 눈 가리고 아웅? 소비자를 뭘로 보는 거야!", "👎 실망이다. 신제품 안 사!"],
                "final_message": "문제의 본질을 외면한 시선 돌리기는 통하지 않았습니다. 소비자들의 불신은 더욱 커졌고, 기업의 미래는 불투명합니다... 📉"
            }
        ]
    }
}

# --- 게임 시작 화면 ---
if st.session_state.game_state == 'start':
    st.markdown("<h1 class='main-title'>🔥 파이어 파이터 PR: 기업을 구하라! 🔥</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>위기 상황 속에서 당신의 PR 능력을 시험해보세요!</p>", unsafe_allow_html=True)
    
    st.image("https://images.pexels.com/photos/17235085/pexels-photo-17235085.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", 
             caption="긴급상황! PR 팀장님 출동! 삐약삐약!", 
             use_column_width=True) 
    st.write("")
    # 여기 '게임 시작' 버튼에 명시적인 key 추가
    if st.button("🚨 게임 시작! PR 팀장이 되어 기업을 구하자! 🚨", use_container_width=True, key="start_game_button"): # <--- 수정된 부분
        st.session_state.game_state = 'stage1'
        st.session_state.current_stage = 1
        st.session_state.accumulated_effects = {'stock_multiplier': 1.0, 'news_headlines': [], 'consumer_sentiment': []}
        st.session_state.last_choice_id = None
        st.rerun()

# --- 1단계 게임 진행 ---
elif st.session_state.game_state == 'stage1':
    st.markdown(f"<p class='stage-indicator'>----- ✨ 1단계: 초기 대응 ✨ -----</p>", unsafe_allow_html=True)
    current_scenario = game_data["stage1"]
    st.markdown(f"<div class='scenario-box'><h3>{current_scenario['title']}</h3><p>{current_scenario['description']}</p></div>", unsafe_allow_html=True)

    cols = st.columns(len(current_scenario['choices']))
    for i, choice in enumerate(current_scenario['choices']):
        with cols[i]:
            if st.button(choice['text'], key=f"s1_choice_{i}", use_container_width=True):
                st.session_state.accumulated_effects['stock_multiplier'] *= choice['effect_stock_multiplier']
                st.session_state.accumulated_effects['news_headlines'].append(choice['effect_news'])
                st.session_state.accumulated_effects['consumer_sentiment'].extend(random.sample(choice['effect_consumer'], min(2, len(choice['effect_consumer']))))
                st.session_state.last_choice_id = choice['id']
                st.session_state.game_state = 'stage2'
                st.session_state.current_stage = 2
                st.rerun()

# --- 2단계 게임 진행 ---
elif st.session_state.game_state == 'stage2':
    st.markdown(f"<p class='stage-indicator'>----- ✨ 2단계: 후속 조치와 여론 관리 ✨ -----</p>", unsafe_allow_html=True)

    if st.session_state.last_choice_id == "s1_choice1_recall":
        current_scenario = game_data["stage2_after_recall"]
    elif st.session_state.last_choice_id == "s1_choice2_deny":
        current_scenario = game_data["stage2_after_deny"]
    elif st.session_state.last_choice_id == "s1_choice3_investigate":
        current_scenario = game_data["stage2_after_investigate"]
    else:
        st.error("이전 단계 선택 오류 발생!")
        st.stop()

    st.markdown(f"<div class='scenario-box'><h3>{current_scenario['title']}</h3><p>{current_scenario['description']}</p></div>", unsafe_allow_html=True)

    cols = st.columns(len(current_scenario['choices']))
    for i, choice in enumerate(current_scenario['choices']):
        with cols[i]:
            if st.button(choice['text'], key=f"s2_choice_{i}", use_container_width=True):
                st.session_state.accumulated_effects['stock_multiplier'] *= choice['effect_stock_multiplier']
                st.session_state.accumulated_effects['news_headlines'].append(choice['effect_news'])
                st.session_state.accumulated_effects['consumer_sentiment'].extend(random.sample(choice['effect_consumer'], min(2, len(choice['effect_consumer']))))
                st.session_state.final_message = choice['final_message']
                st.session_state.game_state = 'result'
                st.rerun()

# --- 결과 화면 ---
elif st.session_state.game_state == 'result':
    initial_stock_price = 10000
    final_stock_price = initial_stock_price * st.session_state.accumulated_effects['stock_multiplier']
    
    st.markdown("<h1 class='result-header'>🎉 최종 결과: 당신의 선택이 기업의 운명을 바꿨다! 🎉</h1>", unsafe_allow_html=True)
    st.write("---")

    st.markdown("<h2 class='result-section-title'>🚨 [속보] 지금 막 들어온 뉴스 헤드라인!</h2>", unsafe_allow_html=True)
    for news in st.session_state.accumulated_effects['news_headlines']:
        with st.spinner("언론사에서 기사를 송고하고 있습니다..."):
            time.sleep(1.5)
        st.markdown(f"<div class='news-box'>➡️ {news}</div>", unsafe_allow_html=True)
        time.sleep(0.5)
    st.write("")

    st.markdown("<h2 class='result-section-title'>📈 긴급 분석: '맛나요 식품' 주가 대변동?!</h2>", unsafe_allow_html=True)
    with st.spinner("증권가에서 급변하는 주가 정보를 분석 중입니다..."):
        time.sleep(2)
    stock_change_percent = (final_stock_price / initial_stock_price - 1) * 100
    stock_emoji = "📈" if stock_change_percent >= 0 else "📉"
    stock_color_class = "stock-up" if stock_change_percent >= 0 else "stock-down"

    st.markdown(f"<div class='stock-box'>", unsafe_allow_html=True)
    st.markdown(f"**💰 시뮬레이션 시작 주가:** <span class='stock-value'>₩{initial_stock_price:,.0f}</span>", unsafe_allow_html=True)
    st.markdown(f"**💰 최종 결과 주가:** <span class='stock-value'>₩{final_stock_price:,.0f}</span>", unsafe_allow_html=True)
    st.markdown(f"**📈 주가 변동률:** <span class='stock-change {stock_color_class}'>{stock_emoji} {stock_change_percent:+.1f}%</span>", unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("<h2 class='result-section-title'>🗣️ 핫이슈: SNS 소비자 반응 폭주!</h2>", unsafe_allow_html=True)
    with st.spinner("소셜 미디어 분석 시스템이 여론을 수집 중입니다..."):
        time.sleep(2.5)
    st.markdown(f"<div class='consumer-box'>", unsafe_allow_html=True)
    random.shuffle(st.session_state.accumulated_effects['consumer_sentiment'])
    for reaction in st.session_state.accumulated_effects['consumer_sentiment']:
        st.markdown(f"💬 {reaction}")
        time.sleep(0.3)
    st.markdown(f"</div>", unsafe_allow_html=True)
    st.write("")

    st.markdown("---")
    st.markdown(f"<p class='final-message'>{st.session_state.final_message}</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.write("")
    # 여기 '다시 플레이하기' 버튼의 key를 명확히 하고, 조건 밖으로 빼도 무방
    if st.button("🔄 다시 플레이하기! 기업을 구하러 한 번 더! 🔄", use_container_width=True, key="restart_game_button_final"): # <--- 수정된 부분 (key 변경)
        st.session_state.game_state = 'start'
        st.session_state.current_stage = 1
        st.session_state.accumulated_effects = {'stock_multiplier': 1.0, 'news_headlines': [], 'consumer_sentiment': []}
        st.session_state.last_choice_id = None
        st.experimental_rerun()
