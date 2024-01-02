**사전준비**

# virtual environment 생성 (프로젝트 격리)

python -m venv ./env

# 환경 접속 (powershell 기준)

<venv>\Scripts\Activate.ps1 (shell 권한 변경 필요)

# requirements.txt 추가

# https://gist.github.com/serranoarevalo/72d77c36dde1cc3ffec34105eb666140

(env) PS C:\project\gpt> pip install -r requirements.txt

**home**

- streamlit run home.py

**sample**
**konlpy 설치문제로 docker image 활용**

- https://github.com/hard-coders/konlpy

**test in powerShell**

- docker run -it --rm -v ${pwd}/test.py:/home/test.py rurouni24/konlpy:python3.7 /bin/bash
