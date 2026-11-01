# 파이썬 함정 퀴즈 (초안)

수업에서 배운 시험 함정으로 문제를 내고, 채점하고, 복습할 주제를 알려 주는 웹앱입니다.

## 실행 방법
```
pip install flask
python app.py
```
브라우저에서 http://127.0.0.1:5000 을 엽니다. 웹 없이 콘솔로 풀려면 `python quiz.py`.

## 파일 역할
| 파일 | 하는 일 | 쓴 문법 |
|---|---|---|
| `questions.py` | 문제 12개 (문제 하나 = 딕셔너리, 전체 = 리스트) | dict, list |
| `quiz.py` | 주제별 문제 고르기, 채점, 등급, 복습 조언, 콘솔 버전 `main()` | 함수, for, if/elif, try/except ValueError |
| `app.py` | 웹 화면 3개 (주제 선택 → 문제 → 채점 결과) | Flask (수업 범위 밖, 이 파일에만) |
| `static/style.css` | 화면 디자인 (교범 문서 스타일: 올리브색, 문단 번호, "평가 완료" 도장). 글꼴은 Google Fonts에서 받으므로 인터넷이 없으면 기본 글꼴로 보임 | CSS |

## 핵심 아이디어 (발표용 한 줄)
채점·조언 로직은 전부 `quiz.py`에 배운 파이썬으로만 있고, `app.py`는 그 함수를 웹에서 부르기만 한다.

예: 학습 도우미 `get_advice(wrong)`는 틀린 문제의 주제를 딕셔너리로 세서 가장 많이 틀린 주제를 알려 준다.
```python
counts = {}
for q in wrong:
    if q["topic"] in counts:
        counts[q["topic"]] = counts[q["topic"]] + 1
    else:
        counts[q["topic"]] = 1
```

## 범위 밖으로 쓴 것 (발표 때 알고 있으면 좋음)
- `flask`: 웹 서버. `@app.route("/")`는 "이 주소로 오면 아래 함수를 실행해라"라는 뜻.
- `html.escape`: 문제 코드 속 `<`, `"` 같은 글자가 화면을 깨지 않게 바꿔 주는 표준 함수.

## 휴대폰으로 열기
1. PC와 휴대폰을 **같은 Wi-Fi**에 연결합니다.
2. PC에서 `python app.py`를 실행합니다.
3. PC의 IP 주소를 찾습니다.
   - Windows: 명령 프롬프트에서 `ipconfig` → "IPv4 주소" (예: `192.168.0.15`)
   - Mac: 시스템 설정 → Wi-Fi → 연결된 네트워크의 "세부사항" → IP 주소
4. 휴대폰 브라우저에서 `http://192.168.0.15:5000` 처럼 입력합니다.
5. 안 열리면: Windows 방화벽 알림이 뜰 때 "허용"을 누르거나, 학교·부대 Wi-Fi처럼 기기끼리 연결을 막는 망이면 휴대폰 핫스팟에 PC를 연결해 봅니다.

## 인터넷 어디서나 열기 (PythonAnywhere 무료)
1. pythonanywhere.com 가입 (무료 Beginner 계정).
2. Files 탭에서 `app.py`, `quiz.py`, `questions.py`, `static/style.css`를 올립니다.
3. Web 탭 → Add a new web app → Flask 선택.
4. WSGI 설정 파일에서 `from app import app as application` 이 되도록 경로를 맞춥니다.
5. Reload 후 `https://아이디.pythonanywhere.com` 주소로 휴대폰 어디서든 열립니다.

## 창으로 뜨는 프로그램 (exe)
`desktop_app.py`는 같은 `quiz.py`를 tkinter 창 화면으로 보여 주는 버전입니다. 디자인은 웹앱과 같은 교범 스타일입니다.
```
python desktop_app.py                                   # 바로 실행
pip install pyinstaller
pyinstaller --onefile --windowed desktop_app.py         # dist/desktop_app.exe 생성 (Windows에서)
```
- `--windowed`는 검은 콘솔 창 없이 프로그램 창만 띄우는 옵션입니다.
- 처음 실행 시 Windows가 "알 수 없는 앱" 경고를 띄우면 추가 정보 → 실행.
- 범위 밖으로 쓴 것: `tkinter`(창 만들기), `lambda`(버튼을 눌렀을 때 실행할 짧은 함수).
