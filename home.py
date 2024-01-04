import streamlit as st
from login import login
from component import login_component
from testCase import testCaseDivide

# 사이드바 생성
sidebar = st.sidebar
sidebar.header('테스트 봇')

# 사이드바에 텍스트 입력 필드 추가
test_case = sidebar.text_area('테스트 케이스')
expected = sidebar.text_area('기대값')

# 상단의 단일 텍스트 박스 추가
st.header("디버깅")
# step1 = st.text_area("step1 로그인", "", height=100)
# step2 = st.text_area("step2 테스트 케이스 실행", "", height=100)
# step3 = st.text_area("step3 기대값 매칭", "", height=100)

# 사이드바에 버튼 추가
if sidebar.button('버튼 클릭'):
    testCaseDivide(test_case)
    
