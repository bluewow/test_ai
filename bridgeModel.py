from component import *

actions_list = ["로그인", "로그아웃", "클릭", "선택", "체크"]

def conectCaseAndModel(case):
    # action list와 case.action이 일치하면 실행
    if case.action in actions_list:
        if case.action == "로그인":
            execute_with_retry(login_event)
        elif case.action == "로그아웃":
            execute_with_retry(logout_event)
        elif case.action == "클릭":
            execute_with_retry(click_event(case.target))
        elif case.action == "선택":
            # 선택에 대한 동작 수행
            pass
        elif case.action == "체크":
            # 체크에 대한 동작 수행
            pass
    