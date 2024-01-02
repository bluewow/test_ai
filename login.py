from selenium import webdriver
from retrieval import rag

# 로그인
def login():
    # 웹드라이버 초기화 (여기서는 Chrome을 예로 들었습니다)
    driver = webdriver.Chrome()

    driver.get('https://m5-dev.matamath.net')
    # localCache clear
    driver.execute_script("window.localStorage.clear();")
    
    # 로그인할 웹사이트 열기
    rag("https://m5-dev.matamath.net/demo.hs/login", driver)
