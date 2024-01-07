import streamlit as st
from sample.login import login
from testCaseDivider import testCaseDivide
from bridgeModel import conectCaseAndModel
from component import init_driver
import pandas as pd
import time

# 상단의 단일 텍스트 박스 추가
st.header("테스트 봇")

# 테스트 데이터
test_data = {
    "로그인": {
        "테스트 케이스": ["선생님 계정으로 로그인", "로그아웃"],
        "기대값": ["선생님 홈화면으로 이동", "로그인 화면으로 이동"]
    },
    "간편출제 테스트": {
        "테스트 케이스": [
            "로그인 > 마타와 연산학습 클릭",
            "학습범위 선택화면 체크",
            "중1(상) 선택 > 다음 버튼 클릭",
            "1강 선택 > 다음 버튼 클릭", 
            "2023 학년도 선택 > 1학년 선택 > 1학년 1반 선택 > 다음 버튼 클릭", 
            "치료학습지 1회 선택 > 완료 버튼 클릭", 
            "나의 수업 보기 > [마타와 연산학습]중1(상) 선택"
        ],
        "기대값": [
            "학습범위 선택 화면으로 이동",
            "초등학교 범위, 중학교 범위, 고등학교 범위 각 범위가 화면에 표시됨",
            "강의별 유형 선택 화면 이동",
            "학습지 출제 대상 화면으로 이동", 
            "설정사항 화면으로 이동", 
            "출제 완료 화면으로 이동", 
            "수업 상세 화면으로 이동"
        ]
    }
}


# Streamlit 앱에서 표시
st.title("테스트 시나리오 표")

# 데이터프레임 생성을 위한 준비
rows = []
for scenario, content in test_data.items():
    test_cases = content["테스트 케이스"]
    expected_values = content["기대값"]

    for i in range(max(len(test_cases), len(expected_values))):
        test_case = test_cases[i] if i < len(test_cases) else ""
        expected_value = expected_values[i] if i < len(expected_values) else ""
        rows.append([scenario, test_case, expected_value])

# 데이터프레임 생성
df = pd.DataFrame(rows, columns=["테스트 시나리오", "테스트 케이스", "기대값"])


# 사용자 입력
selected_scenario = st.selectbox('테스트 시나리오 선택', df['테스트 시나리오'].unique())

# 선택된 시나리오에 대한 데이터 검색
filtered_data = df[df['테스트 시나리오'] == selected_scenario]

# 결과 표시
if not filtered_data.empty:
    st.write('테스트 케이스 및 기대값:')
    st.table(filtered_data)
else:
    st.write("선택한 테스트 시나리오에 대한 데이터가 없습니다.")
    
# 예시 데이터
test_scenario = "로그인"
expected_value = "선생님 홈화면으로 이동"

if st.button("테스트 시작"):
    # 사용자가 선택한 시나리오에 대한 데이터 검색
    if selected_scenario in test_data:
        selected_test_cases = test_data[selected_scenario]["테스트 케이스"]
        selected_expected_values = test_data[selected_scenario]["기대값"]
        print('start : ', selected_test_cases)

        init_driver()
        for test_case in selected_test_cases:
            cases = testCaseDivide(test_case)
            for case in cases:
                print('-----', case.target, case.action, '-----')
                conectCaseAndModel(case)
                time.sleep(3)
    else:
        st.write("선택한 테스트 시나리오에 대한 데이터가 없습니다.")
    
    
