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
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


max_retries = 3  # 최대 재시도 횟수
retry_count = 0  # 현재 재시도 횟수
# gpt-3.5-turbo-16k
chatModel = ChatOpenAI(temperature=0.1, max_tokens=2048, model_name='gpt-3.5-turbo-16k')
driver = None

def init_driver():
    global driver
    driver = webdriver.Chrome()

def remove_script_tags(html_content):
    if not isinstance(html_content, str):
        html_content = str(html_content)
        
    # Using regular expression to remove <script>...</script>
    html = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    cleaned_html = re.sub(r'<img[^>]*>.*?</>', '', html, flags=re.DOTALL)
    # print(cleaned_html)
    return cleaned_html

def get_html_body(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        del img['src']
        del img['srcset']
        
    # body 태그의 내용을 추출합니다.
    cleaned_html_text = remove_script_tags(soup.body)
    # print(cleaned_html_text)
    return cleaned_html_text
    
def execute_with_retry(action, target=None, max_retries=3):
    """ 에러 발생 시 재시도를 수행하는 함수 """
    retry_count = 0
    while (retry_count < max_retries):
        try:
            if (target is None):
                action()  # 주어진 작업 실행
            else:
                action(target, retry_count)
            return  # 성공 시 함수 종료
        except Exception as e:
            print(f"에러 발생: {e}", retry_count)
            retry_count += 1
            time.sleep(0.5)

    print("에러----종료")
    driver.quit()            
    exit()

    

    
def login_event():
    global driver

    driver.get("https://m5-dev.matamath.net/demo.hs/login")
    driver.execute_script("window.localStorage.clear();")
    body = get_html_body(driver)
    chat_prompt = ChatPromptTemplate.from_template(
        """로그인을 해야하고 해당 {body} 를 분석하여 json 포맷으로 출력을 원해. 
        키값은 아래와 같아
        id_element, password_element, login_button_element
        각 키의 값은 selenium 4.3.0 버전의 코드야. 
        comma 나 json 문법에 신경써줘
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
                
def logout_event():
    global driver
    
    body = get_html_body(driver)
    chat_prompt = ChatPromptTemplate.from_template(
        """로그아웃을 해야하고 해당 {body} 를 분석하여 json 포맷으로 출력을 원해. 
        키값은 아래와 같아
        logout_element
        각 키의 값은 selenium 4.3.0 버전의 코드야.
        comma 나 json 문법에 신경써줘
        """
    )
    
    chain = chat_prompt | chatModel | SimpleJsonOutputParser()
    json = chain.invoke({"body": body})
    print('json', json)

    logout_element = eval(json["logout_element"])
    logout_element.click()
    
def click_event(target, count):
    global driver
    
    body = get_html_body(driver)
    text = None
    
    if count == 0:
        text = """클릭을 해야하고 해당 {body} 를 분석하여 {target} element 르 찾아줘
        json 포맷으로 출력을 원해. 
        키값은 아래와 같아
        click_element
        각 키의 값은 selenium 4.3.0 버전의 코드이며 driver.find_element(By.XPATH, TODO) 포맷이야
        comma 나 json 문법에 신경써줘
        """
    elif count == 1:
        text = """클릭을 해야하고 해당 html 의 {body} 를 분석해서 {target} element 를 찾아줘 
        찾은 element 는 클릭을 할꺼야
        json 포맷으로 출력원하며
        key = click_element
        value = selenium 4.3.0 버전의 driver.find_element(By.XPATH, TODO) 포맷이야
        """
    elif count == 2:
        text = """클릭을 해야하고 해당 html 의 {body} 를 분석해서 json 포맷으로 출력해
        키값은 아래와 같아
        click_element
        키의 값은 {target} 을 찾는 selenium 4.3.0 버전의 코드이며 driver.find_element(By.XPATH, TODO) 포맷이야
        comma 나 json 문법에 신경써줘
        """
    
    chat_prompt = ChatPromptTemplate.from_template(
       text
    )
    
    chain = chat_prompt | chatModel | SimpleJsonOutputParser()
    json = chain.invoke({"body": body, "target": target})
    print('json', json)
    
    click_element = eval(json["click_element"])
    driver.execute_script("arguments[0].click();", click_element)

    # click_element.send_keys(Keys.ENTER)
    # click_element.click()
    
    