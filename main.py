import streamlit as st

def run_app():
    st.title("💖 MBTI 이상형 연예인 추천기 💖")
    st.write("당신의 MBTI 유형에 딱 맞는 이상형 연예인을 찾아보세요!")

    # MBTI 유형 리스트 정의
    mbti_types = [
        "선택해주세요", # 기본값
        "ISTJ", "ISFJ", "INFJ", "INTJ",
        "ISTP", "ISFP", "INFP", "INTP",
        "ESTP", "ESFP", "ENFP", "ENTP",
        "ESTJ", "ESFJ", "ENFJ", "ENTJ"
    ]

    # 각 MBTI 유형별 이상형 연예인 (예시)
    # 이 부분은 재미를 위해 임의로 매칭한 것이니, 자유롭게 변경하셔도 됩니다!
    ideal_celebrities = {
        "ISTJ": "공유 (성실하고 신뢰감 있는 매력)",
        "ISFJ": "아이유 (따뜻하고 배려심 깊은 모습)",
        "INFJ": "RM (방탄소년단) (깊이 있는 생각과 따뜻한 통찰력)",
        "INTJ": "이진혁 (냉철한 분석력과 자기 주관이 뚜렷한 리더)",
        "ISTP": "제이홉 (방탄소년단) (실용적이고 자유로운 에너지를 가진)",
        "ISFP": "박보검 (부드럽고 감성적인 예술가적 면모)",
        "INFP": "태연 (소녀시대) (이상적이고 섬세한 감성을 지닌)",
        "INTP": "조승우 (논리적이고 호기심 넘치는 지성미)",
        "ESTP": "제시 (넘치는 에너지와 거침없는 솔직함)",
        "ESFP": "화사 (마마무) (넘치는 끼와 유쾌함으로 분위기 메이커)",
        "ENFP": "뷔 (방탄소년단) (자유분방하고 매력적인 에너지)",
        "ENTP": "덱스 (창의적이고 도전적인 모험가)",
        "ESTJ": "박서준 (체계적이고 추진력 있는 카리스마)",
        "ESFJ": "유재석 (따뜻하고 사람들을 잘 챙기는 사회생활의 달인)",
        "ENFJ": "박보영 (사람을 이끄는 포용력과 긍정적인 영향력)",
        "ENTJ": "카이 (EXO) (강한 리더십과 목표 지향적인 추진력)"
    }

    # MBTI 유형 선택 드롭다운 메뉴
    selected_mbti = st.selectbox("당신의 MBTI 유형을 선택해주세요:", mbti_types)

    # 결과 표시
    if selected_mbti != "선택해주세요":
        if selected_mbti in ideal_celebrities:
            st.success(f"💖 당신의 MBTI 유형 **{selected_mbti}**에 어울리는 이상형 연예인은 바로...")
            st.header(f"✨ {ideal_celebrities[selected_mbti]} ✨")
            st.markdown("---")
            st.info("이 추천은 재미를 위한 예시이며, 실제 인물이나 과학적 근거와는 무관합니다.")
        else:
            st.warning("선택하신 MBTI 유형에 대한 정보가 아직 없어요. 개발자에게 문의해주세요!")
    else:
        st.info("위에서 당신의 MBTI 유형을 선택해주세요! ⬆️")

# 앱 실행
if __name__ == "__main__":
    run_app()
