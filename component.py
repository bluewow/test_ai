import time
from dotenv import load_dotenv
load_dotenv()
from selenium import webdriver
from langchain.chat_models import ChatOpenAI
from bs4 import BeautifulSoup
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from selenium.webdriver.common.by import By

max_retries = 3  # 최대 재시도 횟수
retry_count = 0  # 현재 재시도 횟수
chatModel = ChatOpenAI(temperature=0.1, max_tokens=2048, model_name='gpt-3.5-turbo-16k')
driver = None

def init_driver():
    global driver
    driver = webdriver.Chrome()

def get_html_body(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # body 태그의 내용을 추출합니다.
    return soup.body
    

def login_component():
    global driver
    global max_retries 
    global retry_count 
    # 웹드라이버 초기화 (여기서는 Chrome을 예로 들었습니다)
    driver.get("https://m5-dev.matamath.net/demo.hs/login")
    driver.execute_script("window.localStorage.clear();")
    time.sleep(1)
   
    body = get_html_body(driver)
    
    while retry_count < max_retries:
        try:
            chat_prompt = ChatPromptTemplate.from_template(
                """로그인을 해야하고 해당 {body} 를 분석하여 json 포맷으로 출력을 원해. 
                키값은 아래와 같아
                id_element, password_element, login_button_element
                각 키의 값은 selenium 4.3.0 버전의 코드야. 특수문자 escape 조심하고
                """
            )
            chain = chat_prompt | chatModel | SimpleJsonOutputParser()
            json = chain.invoke({"body": body})
            print(json)
            
            id_input = eval(json["id_element"])
            password_input = eval(json["password_element"])
            login_button = eval(json["login_button_element"])
            
            # 사용자 ID와 비밀번호를 입력 필드에 넣습니다.
            id_input.send_keys("demo")
            password_input.send_keys("1234")
            login_button.click()
            retry_count = 0
            break
        except Exception as e:
            print(f"에러 발생: {e}", retry_count)
            retry_count += 1
            time.sleep(0.5)  # 재시도 사이에 간단한 대기 시간

def logout_component():
    global driver
    global max_retries 
    global retry_count 
    
    body = get_html_body(driver)
    
    while retry_count < max_retries:
        try:
            chat_prompt = ChatPromptTemplate.from_template(
                """로그아웃을 해야하고 해당 {body} 를 분석하여 json 포맷으로 출력을 원해. 
                키값은 아래와 같아
                logout_element
                각 키의 값은 selenium 4.3.0 버전의 코드야. 특수문자 escape 조심하고
                """
            )
            
            chain = chat_prompt | chatModel | SimpleJsonOutputParser()
            json = chain.invoke({"body": body})
            print('json', json)
    
            logout_element = eval(json["logout_element"])
            logout_element.click()
            break
        except Exception as e:
            print(f"에러 발생: {e}", retry_count)
            retry_count += 1
            time.sleep(0.5)  # 재시도 사이에 간단한 대기 시간
    
    
 