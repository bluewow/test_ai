# 테스트 케이스 target - action
class TestCase:
    def __init__(self, target, action):
        self.target = target
        self.action = action
    
# 행위로 분류할 단어 리스트
actions_list = ["로그인", "로그아웃", "클릭", "선택", "체크"]

def testCaseDivide(test_case):
    # 결과를 저장할 리스트
    results = []
    
    # 테스트 케이스 자르기
    parts = test_case.split(">")
    for part in parts:
        words = part.split(" ")
        target = []
        action = []
        for word in words:
            # 타겟과 행위 추출
            if word in actions_list:
                action.append(word)
            else:
                target.append(word)
            
        # TestCase 인스턴스 생성
        case = TestCase(' '.join(target), ' '.join(action))
    
        # 결과 저장
        results.append(case)
        target = []
        action = []
        
    # # 결과 출력
    for case in results:
        print(f"Target: {case.target}, Action: {case.action}")