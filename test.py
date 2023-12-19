from konlpy.tag import Okt

# 행위로 분류할 단어 리스트
actions_list = ["로그인", "로그아웃", "클릭", "선택"]

# Okt 형태소 분석기 인스턴스 생성
okt = Okt()

# 분석할 문장들
texts = ["선생님 계정으로 로그인", "로그아웃 ", "홈화면 > 마타와 연산학습 클릭", "학습범위 선택화면 체크", "중1(상) 선택 > 다음 버튼 클릭", "1강 선택 > 다음 버튼 클릭", "2023 학년도 선택 > 1학년 선택 > 1학년 1반 선택 > 다음 버튼 클릭", "치료학습지 1회 선택 > 완료 버튼 클릭", "나의 수업 보기 > [마타와 연산학습]중1(상) 선택"]

# 결과를 저장할 리스트
results = []

for text in texts:
    # '>' 기호를 사용하여 문장을 부분으로 나눔
    parts = text.split(">")

    part_results = []
    for part in parts:
        # 각 부분에 대해 형태소 분석
        tokens = okt.pos(part.strip())

        # 타겟과 행위 추출
        target = []
        action = []

        for word, tag in tokens:
            if word in actions_list:  # actions_list에 있는 단어들은 행위로 간주
                action.append(word)
            elif tag in ["Verb"]:  # 동사
                action.append(word)
            elif tag in ["Noun"]:  # 명사
                target.append(word)
            else:
                if target:
                    target[-1] += word
                else:
                    target.append(word)

        part_results.append({"target": ' '.join(target), "action": action})

    # 결과 저장
    results.append({"text": text, "parts": part_results})

# 결과 출력
for result in results:
    print(f"Text: {result['text']}")
    for part in result["parts"]:
        print(f"  Target: {part['target']}, Action: {' '.join(part['action'])}")
    print()