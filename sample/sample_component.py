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

chatModel = ChatOpenAI(temperature=0.1, max_tokens=2048, model_name='gpt-3.5-turbo-16k')

def sample_login_component():
    # 웹드라이버 초기화 (여기서는 Chrome을 예로 들었습니다)
    driver = webdriver.Chrome()

    driver.get('https://m5-dev.matamath.net')
    # localCache clear
    driver.execute_script("window.localStorage.clear();")
    
    driver.get("https://m5-dev.matamath.net/demo.hs/login")
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # body 태그의 내용을 추출합니다.
    body = soup.body

    chat_prompt = ChatPromptTemplate.from_template(
        """로그인을 해야하고 해당 {body} 를 분석하여 json 포맷으로 출력을 원해. 
        키값은 아래와 같아
        id_element, password_element, login_button_element
        각 키의 값은 selenium 4.3.0 버전의 코드야
        """
    )
    chain = chat_prompt | chatModel | SimpleJsonOutputParser()
    json = chain.invoke({"body": body})
    print(json)
    
    id_input = eval(json["id_element"])
    password_input = eval(json["password_element"])
    login_button = eval(json["login_button_element"])
    
    # # 사용자 ID와 비밀번호를 입력 필드에 넣습니다.
    id_input.send_keys("demo")
    password_input.send_keys("1234")
    time.sleep(5)
    # # 로그인 버튼 클릭
    login_button.click()
    time.sleep(5)