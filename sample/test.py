# from konlpy.tag import Okt
class TestCase:
    def __init__(self, target, action):
        self.target = target
        self.action = action
    
# 분석할 문장들
texts = ["선생님 계정으로 로그인", "로그아웃 ", "로그인 >  마타와 연산학습 클릭", "학습범위 선택화면 체크", "중1(상) 선택 > 다음 버튼 클릭", "1강 선택 > 다음 버튼 클릭", "2023 학년도 선택 > 1학년 선택 > 1학년 1반 선택 > 다음 버튼 클릭", "치료학습지 1회 선택 > 완료 버튼 클릭", "나의 수업 보기 > [마타와 연산학습]중1(상) 선택"]

# 행위로 분류할 단어 리스트
actions_list = ["로그인", "로그아웃", "클릭", "선택", "체크"]

# 결과를 저장할 리스트
results = []

for text in texts:
    # '>' 기호를 사용하여 문장을 부분으로 나눔
    parts = text.split(" > ")

    part_results = []
    for part in parts:
        # 토큰 분리 (형태소 분석 대신 단순 분리 사용)
        tokens = part.split()

        # 타겟과 행위 추출
        target = []
        action = []

        for token in tokens:
            if token in actions_list:
                action.append(token)
            else:
                target.append(token)

        # TestCase 인스턴스 생성
        case = TestCase(' '.join(target), ' '.join(action))
        part_results.append(case)

    # 결과 저장
    results.append(part_results)

# 결과 출력
for result in results:
    for case in result:
        print(f"Target: {case.target}, Action: {case.action}")
    print()