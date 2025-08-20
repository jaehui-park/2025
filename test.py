import streamlit as st
import random
import time # 결과를 단계적으로 보여주기 위해

st.set_page_config(layout="wide", page_title="🔥 파이어 파이터 PR: 기업을 구하라! (심화편) 🔥", initial_sidebar_state="collapsed")

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
    padding: 10px 0;
    border-top: 2px dashed #ADD8E6;
    border-bottom: 2px dashed #ADD8E6;
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
    st.session_state.game_state = 'start' # 'start', 'stage1', 'stage2', 'stage3', 'result'
    st.session_state.current_stage = 1
    st.session_state.accumulated_effects = {'stock_multiplier': 1.0, 'news_headlines': [], 'consumer_sentiment': []}
    st.session_state.last_choice_id = None # 이전 선택의 ID를 저장
    st.session_state.current_stage2_scenario = None # 2단계 시나리오 키 저장

# --- 게임 데이터 정의 ---
game_data = {
    # -------------------------- Stage 1 --------------------------
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
                "next_stage_scenario_key": "stage2_after_recall"
            },
            {
                "id": "s1_choice2_deny",
                "text": "🙅‍♀️ 선택 2: 강력 부인! '악의적인 루머' 법적 대응 예고!",
                "effect_news": "🚨'맛나요 식품', 이물질 논란 '루머'로 치부... 법적 대응 예고에 여론 '부글부글'!",
                "effect_stock_multiplier": 0.70, # 30% 하락
                "effect_consumer": ["😡 이물질이 나왔는데 오리발이라니! 불매운동 갑니다!", "🤬 뻔뻔하다! 소비자를 기만하는 기업은 망해야지!", "👎 이제 맛나요 식품은 걸러야겠다. 진짜 실망이네."],
                "next_stage_scenario_key": "stage2_after_deny"
            },
            {
                "id": "s1_choice3_investigate",
                "text": "🕰️ 선택 3: 진상 규명 선행! '내부 조사 후 발표' 신중론!",
                "effect_news": "⏱️'맛나요 식품', 이물질 논란에 '조사 중'만 반복… 해명 늦어져 불확실성 증폭!",
                "effect_stock_multiplier": 0.85, # 15% 하락
                "effect_consumer": ["🤔 조사 중이라니... 일단 지켜봐야지.", "😩 아니, 그래서 이물질이 진짜 나왔다는 거야 안 나왔다는 거야?", "💬 답답하네! 이러다 사람들 다 떠나가겠다."],
                "next_stage_scenario_key": "stage2_after_investigate"
            }
        ]
    },
    # -------------------------- Stage 2 --------------------------
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
                "next_stage_scenario_key": "stage3_recall_success_path"
            },
            {
                "id": "s2r_choice2_promotion",
                "text": "💰 선택 2: 대규모 할인 프로모션 및 신제품 출시로 분위기 전환 시도!",
                "effect_news": "📉'맛나요 식품', '잊으세요' 식 대규모 할인... 본질 해결 없는 눈속임 비판도!",
                "effect_stock_multiplier": 0.98, # 주가 소폭 하락
                "effect_consumer": ["😒 눈가리고 아웅? 할인해도 불안해서 못 사먹겠다.", "💬 본질적인 문제가 해결된 건가요?", "😠 세일만 하면 다인가? 기만적이다!"],
                "next_stage_scenario_key": "stage3_recall_promotion_fail_path"
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
                "next_stage_scenario_key": "stage3_deny_belated_apology_path"
            },
            {
                "id": "s2d_choice2_fight",
                "text": "⚔️ 선택 2: 끝까지 루머와 싸우겠다! 초강력 법적 대응 돌입!",
                "effect_news": "💣'맛나요 식품', 사과 대신 '전쟁' 선포... 불매운동 확산, 기업 존립 '빨간불'!",
                "effect_stock_multiplier": 0.50, # 50% 폭락
                "effect_consumer": ["🔥 역시 노답이네! 이쯤 되면 망하는 게 답.", "🚨 정부 뭐하냐? 저런 기업 가만 두지 마!", "💀 주식 다 팔았다. 바이바이."],
                "next_stage_scenario_key": "stage3_deny_total_war_path"
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
                "next_stage_scenario_key": "stage3_investigate_late_recovery_path"
            },
            {
                "id": "s2i_choice2_divert",
                "text": "🎭 선택 2: 시선 돌리기! 초대형 신제품 발표회로 분위기 반전 시도!",
                "effect_news": "🎲'맛나요 식품', 위기 속에 신제품 출시 강행... '소비자 기만' 지적 봇물!",
                "effect_stock_multiplier": 0.75, # 25% 추가 하락
                "effect_consumer": ["😠 문제 해결은 안 하고 딴짓하네?", "💬 눈 가리고 아웅? 소비자를 뭘로 보는 거야!", "👎 실망이다. 신제품 안 사!"],
                "next_stage_scenario_key": "stage3_investigate_distraction_fail_path"
            }
        ]
    },
    # -------------------------- Stage 3 --------------------------
    "stage3_recall_success_path": {
        "title": "🏆 3단계 위기: 완벽한 신뢰 회복인가, 방심의 덫인가?",
        "description": """
        탁월한 초기 대응과 투명한 후속 조치로 '맛나요 식품'은 다시 소비자 신뢰를 얻기 시작했습니다. 하지만 이때 발생할 수 있는 '안일함'은 또 다른 위기를 초래할 수 있습니다.
        
        **현재 상황:**
        *   기업 이미지는 역대급으로 긍정적이며, '위기를 기회로 만든 기업'으로 칭송받고 있습니다.
        *   경영진 내부에서는 '이만하면 됐다'는 안도감이 흐르고 있습니다.
        *   그러나 일부에서는 '이물질 사건'이 재발할 수 있다는 우려의 목소리도 남아있습니다. 당신은 마지막으로 무엇에 집중하시겠습니까?
        """,
        "choices": [
            {
                "id": "s3_rs_choice1_constant_vigilance",
                "text": "🌟 선택 1: 재발 방지 시스템 대대적 강화 및 ESG 경영 선포!",
                "effect_news": "🎉'맛나요 식품', 위기를 넘어 '모범 기업'으로! 재발 방지 시스템 혁신, ESG 경영 선포!",
                "effect_stock_multiplier": 1.10, # 추가 상승
                "effect_consumer": ["💖 역시 맛나요! 완벽한 마무리에 감동!", "👏 이런 기업이라면 평생 충성 고객!", "✨ 이대로 쭉 가면 좋겠다!"],
                "final_message": "당신의 탁월한 위기 관리 능력으로 '맛나요 식품'은 이전보다 더욱 강력한 신뢰를 얻는 기업으로 거듭났습니다! PR 전문가로서 최고의 성공을 거두었습니다! 🥳"
            },
            {
                "id": "s3_rs_choice2_brand_expansion",
                "text": "🤑 선택 2: 지금이 기회! '착한 기업' 이미지 활용, 공격적인 마케팅 및 사업 확장!",
                "effect_news": "💸'맛나요 식품', '착한 기업' 이미지로 돈벌이 나서나? 과도한 상업화 논란!",
                "effect_stock_multiplier": 1.03, # 소폭 상승 후 정체
                "effect_consumer": ["😕 좀 벌었다고 너무 티내는 거 아닌가?", "💬 솔직히 감동했지만 너무 상업적이면 실망.", "😒 이젠 돈독만 오른 듯..."],
                "final_message": "위기 극복 후 기업 이미지를 활용해 수익을 늘렸지만, 지나친 상업화로 소비자들의 진정성 의심을 받게 되었습니다. 얻는 것이 있으면 잃는 것도 있습니다. 😐"
            }
        ]
    },
    "stage3_recall_promotion_fail_path": {
        "title": "📉 3단계 위기: 프로모션의 딜레마, 본질은 어디로?",
        "description": """
        리콜 후 대규모 프로모션을 선택했으나, 소비자들은 문제의 본질 해결보다 할인에만 집중한다고 비판하고 있습니다. 주가는 단기적으로 움직였지만, 근본적인 불신은 해소되지 않았습니다.
        
        **현재 상황:**
        *   프로모션에 대한 회의적인 시선과 '소비자 기만'이라는 비판이 커지고 있습니다.
        *   경쟁사들이 '근본적인 품질 개선'을 강조하며 치고 올라오고 있습니다.
        *   직원들 내부에서도 '언제까지 임시방편만 쓸 거냐'는 불만이 제기됩니다. 더 늦기 전에 결정을 내려야 합니다.
        """,
        "choices": [
            {
                "id": "s3_rf_choice1_pivot",
                "text": "🔄 선택 1: 과감하게 정책 전환! 근본적인 품질 관리 혁신 발표!",
                "effect_news": "🛠️'맛나요 식품', 뒤늦게 품질 혁신 선언… '이제라도' vs '이미 늦었다' 엇갈린 시선!",
                "effect_stock_multiplier": 0.90, # 소폭 회복 시도
                "effect_consumer": ["🥺 그래도 이제라도 고치겠다니... 기회 줄까?", "💬 진짜 바뀌면 좋겠지만, 믿기가 힘들다.", "🙏 포기하지 않는 모습은 좋네."],
                "final_message": "뒤늦게나마 품질 개선으로 정책을 전환했지만, '골든 타임'을 놓친 여파가 큽니다. 신뢰 회복에는 많은 시간과 노력이 필요할 것입니다. 💪"
            },
            {
                "id": "s3_rf_choice2_ignore",
                "text": "😡 선택 2: 대수롭지 않게! '노이즈 마케팅' 일환이라며 무대응!",
                "effect_news": "🤬'맛나요 식품', 소비자 비난에 '노이즈 마케팅' 뻔뻔 주장… 최악의 상황 직면!",
                "effect_stock_multiplier": 0.70, # 추가 하락
                "effect_consumer": ["🔥 더 이상 실드 불가. 망해라!", "💀 소비자를 얼마나 우습게 알면 저러지?", "😭 다시는 맛나요 식품 제품 안 사!"],
                "final_message": "소비자들의 분노를 무시한 오만한 태도로 '맛나요 식품'은 치명적인 불신에 빠졌습니다. 회생하기 어려운 상황에 놓였습니다. 💀"
            }
        ]
    },
    "stage3_deny_belated_apology_path": {
        "title": "😟 3단계 위기: 뒤늦은 사과, 통할까?",
        "description": """
        강력 부인 전략의 역풍을 맞아 뒤늦게 사과를 했습니다. 하지만 이미 굳어진 부정적인 이미지와 불신을 해소하기란 쉽지 않습니다.
        
        **현재 상황:**
        *   사과문에 대한 진정성 논란이 계속되고 있습니다.
        *   주가도 좀처럼 회복되지 않고, 투자자들의 이탈이 이어지고 있습니다.
        *   불매운동은 여전히 계속되고 있으며, 기업은 벼랑 끝에 몰려 있습니다. 마지막 남은 카드는 무엇일까요?
        """,
        "choices": [
            {
                "id": "s3_da_choice1_full_transparency",
                "text": "🎥 선택 1: 모든 것을 공개한다! 제조 공정 CCTV 24시간 스트리밍 도입!",
                "effect_news": "👀'맛나요 식품', 초강수! 제조 과정 24시간 공개… '소비자 감시'로 신뢰 회복 시도!",
                "effect_stock_multiplier": 0.98, # 약간의 회복 가능성
                "effect_consumer": ["😮 진짜 한다고? 일단 지켜볼게.", "💬 엄청난 승부수네. 효과 있을까?", "🤔 솔직히 너무 늦었지만... 대단하다."],
                "final_message": "파격적인 시도로 불신을 뚫어내려 노력했습니다. 하지만 이미 너무 깊어진 상처라 완벽한 회복에는 긴 시간이 필요할 것입니다. 지켜보는 소비자들의 시선이 따갑습니다. 😥"
            },
            {
                "id": "s3_da_choice2_give_up_pr",
                "text": "🚶‍♂️ 선택 2: PR은 실패했다! 이젠 사업 재편, 기업 구조조정으로 승부!",
                "effect_news": "💸'맛나요 식품', 사실상 PR 포기… 대규모 구조조정, 사업 축소 돌입! '사실상 백기 투항'!",
                "effect_stock_multiplier": 0.80, # 더 하락
                "effect_consumer": ["💔 결국 자포자기네.", "😭 이럴 줄 알았다. 진작 잘했어야지.", "💀 회사 망하는 소리가 들린다."],
                "final_message": "PR을 포기하고 기업 구조 자체를 바꾸려 했습니다. 이는 사실상 위기 관리 실패를 인정하는 것과 같습니다. 기업은 막대한 손실을 감당해야 할 것입니다. 📉"
            }
        ]
    },
    "stage3_deny_total_war_path": {
        "title": "💀 3단계 위기: 최악의 결과, 기업의 종말?",
        "description": """
        끝까지 법적 대응을 선택하며 소비자와의 전쟁을 선포한 결과, 기업은 회생 불가능한 지경에 이르렀습니다. 시장과 소비자 모두 '맛나요 식품'에 등을 돌렸습니다.
        
        **현재 상황:**
        *   불매운동은 전국민적 운동으로 확산되었고, 매출은 제로에 가깝습니다.
        *   직원들은 대거 이탈하고 있으며, 은행 대출마저 막혔습니다.
        *   기업 존폐의 기로, 더 이상 선택지가 남아있을까요? 아니면 기적을 바라야 할까요?
        """,
        "choices": [
            {
                "id": "s3_dt_choice1_ceo_resignation",
                "text": "😭 선택 1: 마지막 발버둥… CEO 사퇴 및 전면 대국민 사과방송 진행!",
                "effect_news": "📢'맛나요 식품' CEO, 뒤늦은 사퇴… 국민 분노 극에 달해, 기업 회생 사실상 '불가능' 판정!",
                "effect_stock_multiplier": 0.60, # 소폭 회복 시도하지만 미미
                "effect_consumer": ["🤦‍♀️ 이미 늦었어.", "💬 눈물 흘린다고 될 일인가.", "😡 사과할 기회 많았잖아!"],
                "final_message": "최후의 수단을 썼지만, 이미 때는 너무 늦었습니다. 기업의 회생은 사실상 불가능하며, 시장에서 퇴출될 위기에 처했습니다. 끔찍한 PR 재앙입니다. ☠️"
            },
            {
                "id": "s3_dt_choice2_bankruptcy",
                "text": "😵 선택 2: 더 이상은 무리다! 파산 신청!",
                "effect_news": "⚰️'맛나요 식품', 끝내 파산 신청… '국민 스낵'의 비극적인 최후, PR 실패의 대명사로 기록!",
                "effect_stock_multiplier": 0.01, # 거의 0
                "effect_consumer": ["🎉 잘 망했다!", "🍾 소비자 기만하면 이렇게 되는구나!", "💖 사필귀정!"],
                "final_message": "당신의 선택으로 '맛나요 식품'은 돌이킬 수 없는 파국의 길을 걸었습니다. 비극적인 PR 실패 사례로 역사에 기록될 것입니다. 게임 오버. 😵"
            }
        ]
    },
    "stage3_investigate_late_recovery_path": {
        "title": "🐌 3단계 위기: 잃어버린 '골든 타임'의 대가",
        "description": """
        늦었지만 투명하게 조사 결과를 공개하고 개선책을 발표했지만, 이미 소비자들은 지칠 대로 지쳐 있습니다. '늑장 대응'이라는 낙인이 찍혔습니다.
        
        **현재 상황:**
        *   대다수의 소비자는 여전히 '맛나요 식품'에 대해 냉담한 반응을 보입니다.
        *   경쟁사들에게 빼앗긴 시장 점유율을 되찾아오기 쉽지 않습니다.
        *   '믿을 수 있는 기업'이라는 이미지를 되찾기 위해 엄청난 시간과 자원이 필요합니다. 당신은 앞으로 어떤 전략으로 이 상황을 헤쳐나갈까요?
        """,
        "choices": [
            {
                "id": "s3_il_choice1_consistent_effort",
                "text": "⏳ 선택 1: 장기적 신뢰 회복! 꾸준한 캠페인과 사회 공헌으로 진정성 증명!",
                "effect_news": "🌱'맛나요 식품', 느리지만 꾸준하게 '재도전'! 소비자들과 소통하며 신뢰의 씨앗 심는다!",
                "effect_stock_multiplier": 1.05, # 느리지만 상승 전환
                "effect_consumer": ["🤔 진정성이 보이기 시작하네... 조금씩 지켜볼까.", "💬 시간은 걸리겠지만, 바뀐다면 응원할게.", "🙏 포기하지 않는 모습은 보기 좋다."],
                "final_message": "잃어버린 '골든 타임'의 대가는 컸지만, 당신의 끈기 있는 노력으로 서서히 신뢰를 회복하는 중입니다. 느리지만 확실한 길을 택했습니다. 미래를 기대해볼 수 있습니다. ✨"
            },
            {
                "id": "s3_il_choice2_rebrand",
                "text": "🎨 선택 2: 이미지 쇄신! 아예 브랜드 이름 바꾸고 리브랜딩 선포!",
                "effect_news": "🔄'맛나요 식품', '잊으세요' 작전 돌입? 회사명까지 바꾸는 '리브랜딩'에 시선 '싸늘'!",
                "effect_stock_multiplier": 0.85, # 다시 하락
                "effect_consumer": ["🙄 이름만 바꾼다고 달라지나?", "💬 문제의 본질은 그대로인데...", "😡 소비자를 얼마나 바보로 아는 거야!"],
                "final_message": "이름만 바꾼다고 과거가 사라지는 것은 아닙니다. 근본적인 문제가 해결되지 않으면 리브랜딩은 실패합니다. 소비자들의 불신은 더욱 깊어졌습니다. 📉"
            }
        ]
    },
    "stage3_investigate_distraction_fail_path": {
        "title": "🎭 3단계 위기: 시선 돌리기의 처참한 결과",
        "description": """
        신중한 조사를 발표하는 대신 신제품 발표회로 시선을 돌리려 했지만, 이는 오히려 소비자들의 비난만 샀습니다. 기업의 무책임함이 만천하에 드러났습니다.
        
        **현재 상황:**
        *   신제품은 '사건 덮으려는 꼼수'라며 판매 부진을 면치 못하고 있습니다.
        *   직원들의 사기는 바닥까지 떨어졌고, 핵심 인력들이 이탈하기 시작했습니다.
        *   기업의 평판은 회복 불가능할 정도로 추락했습니다. 더 이상 기업을 지탱할 수 있을까요?
        """,
        "choices": [
            {
                "id": "s3_id_choice1_scapegoat",
                "text": "✂️ 선택 1: 책임 전가! 담당 임원 해고 및 대국민 사과 발표 (꼬리 자르기)! ",
                "effect_news": "⚡'맛나요 식품', 담당 임원 해고… '꼬리 자르기' 비판 직면, 여론은 여전히 '냉담'!",
                "effect_stock_multiplier": 0.70, # 미미한 회복 시도
                "effect_consumer": ["😒 또 책임 전가냐?", "💬 결국 임원 하나 자르고 끝내려나 보네.", "😡 본질은 그대로인데 누구를 탓해!"],
                "final_message": "책임자를 경질하는 꼬리 자르기식 대처는 소비자들에게 통하지 않았습니다. 근본적인 해결 의지가 없다는 것을 드러낸 꼴이 되어 오히려 더 큰 비난을 받게 되었습니다. 💀"
            },
            {
                "id": "s3_id_choice2_liquidate",
                "text": "🛑 선택 2: 모든 것을 포기! 공장 매각 및 핵심 사업만 남기고 축소!",
                "effect_news": "🚨'맛나요 식품', 사업 대폭 축소! '명예 실추' 속에 간판만 유지하는 신세로 전락!",
                "effect_stock_multiplier": 0.50, # 추가 하락
                "effect_consumer": ["📉 이젠 망했네. ", "💬 불과 몇 년 전만 해도 잘 나갔는데.", "😭 안녕히..."],
                "final_message": "최악의 상황을 더 이상 감당하지 못하고 기업을 대폭 축소하게 되었습니다. 한때 잘나가던 '맛나요 식품'은 명예를 잃고 겨우 명맥만 유지하게 됩니다. 비참한 PR 실패입니다. 💥"
            }
        ]
    }
}


# --- 게임 시작 화면 ---
if st.session_state.game_state == 'start':
    st.markdown("<h1 class='main-title'>🔥 파이어 파이터 PR: 기업을 구하라! (심화편) 🔥</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>위기 상황 속에서 당신의 PR 능력을 시험해보세요!</p>", unsafe_allow_html=True)
    
    st.image("https://images.pexels.com/photos/17235085/pexels-photo-17235085.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", 
             caption="긴급상황! PR 팀장님 출동! 삐약삐약!", 
             use_column_width=True) 
    st.write("")
    if st.button("🚨 게임 시작! PR 팀장이 되어 기업을 구하자! 🚨", use_container_width=True, key="start_game_button"):
        st.session_state.game_state = 'stage1'
        st.session_state.current_stage = 1
        st.session_state.accumulated_effects = {'stock_multiplier': 1.0, 'news_headlines': [], 'consumer_sentiment': []}
        st.session_state.last_choice_id = None
        st.session_state.current_stage2_scenario = None # 초기화
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
                st.session_state.current_stage2_scenario = choice['next_stage_scenario_key'] # 2단계 시나리오 키 저장
                st.session_state.game_state = 'stage2'
                st.session_state.current_stage = 2
                st.rerun()

# --- 2단계 게임 진행 ---
elif st.session_state.game_state == 'stage2':
    st.markdown(f"<p class='stage-indicator'>----- ✨ 2단계: 후속 조치와 여론 관리 ✨ -----</p>", unsafe_allow_html=True)

    current_scenario = game_data[st.session_state.current_stage2_scenario]
    st.markdown(f"<div class='scenario-box'><h3>{current_scenario['title']}</h3><p>{current_scenario['description']}</p></div>", unsafe_allow_html=True)

    cols = st.columns(len(current_scenario['choices']))
    for i, choice in enumerate(current_scenario['choices']):
        with cols[i]:
            if st.button(choice['text'], key=f"s2_choice_{i}", use_container_width=True):
                st.session_state.accumulated_effects['stock_multiplier'] *= choice['effect_stock_multiplier']
                st.session_state.accumulated_effects['news_headlines'].append(choice['effect_news'])
                st.session_state.accumulated_effects['consumer_sentiment'].extend(random.sample(choice['effect_consumer'], min(2, len(choice['effect_consumer']))))
                st.session_state.last_choice_id = choice['id'] # 이번 선택 ID로 갱신
                st.session_state.current_stage3_scenario = choice['next_stage_scenario_key'] # 3단계 시나리오 키 저장
                st.session_state.game_state = 'stage3'
                st.session_state.current_stage = 3
                st.rerun()

# --- 3단계 게임 진행 ---
elif st.session_state.game_state == 'stage3':
    st.markdown(f"<p class='stage-indicator'>----- ✨ 3단계: 최종 결단과 미래 전략 ✨ -----</p>", unsafe_allow_html=True)

    current_scenario = game_data[st.session_state.current_stage3_scenario]
    st.markdown(f"<div class='scenario-box'><h3>{current_scenario['title']}</h3><p>{current_scenario['description']}</p></div>", unsafe_allow_html=True)

    cols = st.columns(len(current_scenario['choices']))
    for i, choice in enumerate(current_scenario['choices']):
        with cols[i]:
            if st.button(choice['text'], key=f"s3_choice_{i}", use_container_width=True):
                st.session_state.accumulated_effects['stock_multiplier'] *= choice['effect_stock_multiplier']
                st.session_state.accumulated_effects['news_headlines'].append(choice['effect_news'])
                st.session_state.accumulated_effects['consumer_sentiment'].extend(random.sample(choice['effect_consumer'], min(2, len(choice['effect_consumer']))))
                st.session_state.final_message = choice['final_message'] # 최종 메시지는 마지막 단계 선택에서 결정
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
    if st.button("🔄 다시 플레이하기! 기업을 구하러 한 번 더! 🔄", use_container_width=True, key="restart_game_button_final"):
        st.session_state.game_state = 'start'
        st.session_state.current_stage = 1
        st.session_state.accumulated_effects = {'stock_multiplier': 1.0, 'news_headlines': [], 'consumer_sentiment': []}
        st.session_state.last_choice_id = None
        st.session_state.current_stage2_scenario = None
        st.rerun()
