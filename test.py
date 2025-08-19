import streamlit as st

st.set_page_config(layout="wide", page_title="우리 기업, 어디까지 알아봤니? 🔎")

# --- 앱 제목 및 소개 ---
st.markdown("<h1 style='text-align: center; color: #FF69B4;'>✨ 우리 기업, 어디까지 알아봤니? ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ADD8E6;'>🔍 쉽고 재미있게 기업의 강점, 약점, 기회, 위협을 분석하고 경쟁사와 비교해봐요! 🚀</h3>", unsafe_allow_html=True)

st.write("") # 간격 추가
st.write("---") # 구분선
st.write("") # 간격 추가

# --- 1. 기업 정보 입력 ---
st.subheader("1️⃣ 분석하고 싶은 기업은 어디인가요? 🏢")
company_name = st.text_input("여기에 기업 이름을 입력해주세요! (예: 삼성전자, 애플, 우리 동네 카페 이름 등)", "멋쟁이기업")

st.write("") # 간격 추가

# --- 2. SWOT 분석 ---
st.subheader(f"2️⃣ '{company_name}'의 SWOT을 분석해볼까요? 🧠")
st.info("💡 SWOT은 Strength(강점), Weakness(약점), Opportunity(기회), Threat(위협)의 줄임말이에요. 기업의 현재 상황과 미래를 분석하는 데 아주 유용한 도구랍니다!")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h4 style='color: #4CAF50;'>💪 Strength (강점)</h4>", unsafe_allow_html=True)
    st.write("기업 내부의 긍정적인 요소를 적어주세요. 이 기업이 가진 최고의 무기는 무엇일까요?")
    swot_s = st.text_area("예: 혁신적인 기술력, 강력한 브랜드 이미지, 우수한 인재들", height=150, key="strength")

with col2:
    st.markdown("<h4 style='color: #FF5722;'>🤏 Weakness (약점)</h4>", unsafe_allow_html=True)
    st.write("기업 내부의 부정적인 요소를 적어주세요. 이 기업이 개선해야 할 점은 무엇일까요?")
    swot_w = st.text_area("예: 높은 생산 비용, 제한적인 시장 접근성, 경직된 조직 문화", height=150, key="weakness")

col3, col4 = st.columns(2)

with col3:
    st.markdown("<h4 style='color: #2196F3;'>🌈 Opportunity (기회)</h4>", unsafe_allow_html=True)
    st.write("기업 외부의 긍정적인 요소를 적어주세요. 이 기업에 찾아올 기회는 무엇일까요?")
    swot_o = st.text_area("예: 새로운 기술 트렌드 부상, 규제 완화, 성장하는 시장 수요", height=150, key="opportunity")

with col4:
    st.markdown("<h4 style='color: #FFC107;'>🌩️ Threat (위협)</h4>", unsafe_allow_html=True)
    st.write("기업 외부의 부정적인 요소를 적어주세요. 이 기업을 위협하는 요소는 무엇일까요?")
    swot_t = st.text_area("예: 치열한 경쟁, 경기 침체, 기술 변화에 따른 새로운 위협", height=150, key="threat")

st.write("") # 간격 추가

# --- 3. 경쟁사 비교 분석 ---
st.subheader(f"3️⃣ '{company_name}'과 주요 경쟁사를 비교해볼까요? 🆚")
st.info("💡 어떤 점들을 기준으로 비교해볼지 정하고, 각 기업이 어떤지 직접 적어보는 거예요!")

st.write("---")

col_comp1, col_comp2 = st.columns(2)

with col_comp1:
    competitor1_name = st.text_input("첫 번째 경쟁사 이름은? (예: 똑쟁이기업)", "경쟁사 A")
with col_comp2:
    competitor2_name = st.text_input("두 번째 경쟁사 이름은? (예: 영리기업)", "경쟁사 B")

st.write("") # 간격 추가

st.write("어떤 기준으로 비교할지 정해봐요! 최소 3개는 입력하는 걸 추천해요! 👇")

comparison_criteria = []
comparison_data = {}

for i in range(5): # 최대 5가지 비교 기준
    col_crit, col_comp_A, col_comp_B, col_comp_C = st.columns([2, 3, 3, 3])
    with col_crit:
        criterion = st.text_input(f"비교 기준 {i+1} (예: 시장 점유율, 기술 혁신, 고객 서비스)", key=f"crit_{i}")
    if criterion:
        comparison_criteria.append(criterion)
        with col_comp_A:
            company_data = st.text_input(f"{company_name}", key=f"compA_data_{i}", help=f"'{company_name}'에 대한 '{criterion}' 정보를 입력해주세요.")
        with col_comp_B:
            comp1_data = st.text_input(f"{competitor1_name}", key=f"compB_data_{i}", help=f"'{competitor1_name}'에 대한 '{criterion}' 정보를 입력해주세요.")
        with col_comp_C:
            comp2_data = st.text_input(f"{competitor2_name}", key=f"compC_data_{i}", help=f"'{competitor2_name}'에 대한 '{criterion}' 정보를 입력해주세요.")

        comparison_data[criterion] = {
            company_name: company_data,
            competitor1_name: comp1_data,
            competitor2_name: comp2_data
        }

st.write("") # 간격 추가
st.write("---")
st.write("") # 간격 추가

# --- 분석 결과 버튼 ---
if st.button("📊 분석 결과 확인하기! 🚀", use_container_width=True):
    st.balloons() # 풍선 효과로 축하!
    st.snow() # 눈 내리는 효과도 함께!

    st.markdown("<h2 style='text-align: center; color: #9B59B6;'>🎉 짜잔! 당신의 멋진 기업 분석 결과예요! 🎉</h2>", unsafe_allow_html=True)
    st.write("")
    st.write("---")
    st.write("")

    # --- SWOT 분석 결과 표시 ---
    st.subheader(f"✨ '{company_name}' SWOT 분석 결과 ✨")

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.markdown("<h4 style='color: #4CAF50;'>💪 Strength (강점)</h4>", unsafe_allow_html=True)
        if swot_s: st.markdown(f"> {swot_s}")
        else: st.info("아직 입력된 강점이 없어요. 채워주시면 더 완벽해질 거예요!")

    with res_col2:
        st.markdown("<h4 style='color: #FF5722;'>🤏 Weakness (약점)</h4>", unsafe_allow_html=True)
        if swot_w: st.markdown(f"> {swot_w}")
        else: st.info("아직 입력된 약점이 없어요. 채워주시면 더 완벽해질 거예요!")

    res_col3, res_col4 = st.columns(2)

    with res_col3:
        st.markdown("<h4 style='color: #2196F3;'>🌈 Opportunity (기회)</h4>", unsafe_allow_html=True)
        if swot_o: st.markdown(f"> {swot_o}")
        else: st.info("아직 입력된 기회가 없어요. 채워주시면 더 완벽해질 거예요!")

    with res_col4:
        st.markdown("<h4 style='color: #FFC107;'>🌩️ Threat (위협)</h4>", unsafe_allow_html=True)
        if swot_t: st.markdown(f"> {swot_t}")
        else: st.info("아직 입력된 위협이 없어요. 채워주시면 더 완벽해질 거예요!")

    st.write("")
    st.write("---")
    st.write("")

    # --- 경쟁사 비교 분석 결과 표시 ---
    st.subheader(f"⚔️ '{company_name}' VS '{competitor1_name}' VS '{competitor2_name}' 비교 분석 🛡️")

    if comparison_criteria:
        # 데이터를 표 형식으로 만들기
        table_data = {"비교 기준": comparison_criteria}
        table_data[company_name] = [comparison_data[crit][company_name] for crit in comparison_criteria]
        table_data[competitor1_name] = [comparison_data[crit][competitor1_name] for crit in comparison_criteria]
        table_data[competitor2_name] = [comparison_data[crit][competitor2_name] for crit in comparison_criteria]

        import pandas as pd
        df_comparison = pd.DataFrame(table_data)
        st.table(df_comparison) # `st.table`은 데이터를 그대로 표시하여 학생들이 이해하기 쉽게 함

    else:
        st.info("아직 비교 기준이나 내용이 입력되지 않았어요. 위에서 입력하고 '분석 결과 확인하기'를 다시 눌러주세요!")

    st.write("")
    st.markdown("<h4 style='text-align: center; color: #008080;'>⭐ 스스로 기업을 분석해내는 모습, 정말 멋져요! ⭐</h4>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #6A5ACD;'>궁금한 기업이 있다면 다시 시작해보세요! 🔁</h5>", unsafe_allow_html=True)

