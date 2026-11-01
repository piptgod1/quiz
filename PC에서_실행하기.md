# PC(Windows)에서 실행하기

처음 한 번만 1~3단계를 하고, 그다음부터는 4단계만 하면 됩니다.

## 1. 파이썬 설치 (처음 한 번)
1. https://www.python.org/downloads 에 들어가 노란 **Download Python 3.x** 버튼을 누릅니다.
2. 받은 설치 파일을 실행합니다.
3. 첫 화면 맨 아래 **Add python.exe to PATH** 를 **꼭 체크**하고 **Install Now** 를 누릅니다.
4. 확인: 시작 메뉴에서 `cmd` 를 검색해 **명령 프롬프트**를 열고 아래를 입력합니다.
   ```
   python --version
   ```
   `Python 3.13.x` 처럼 나오면 성공입니다.

## 2. 코드 받기 (처음 한 번)
1. https://github.com/piptgod1/quiz 에 들어갑니다.
2. 초록색 **Code** 버튼 → **Download ZIP** 을 누릅니다.
3. 받은 `quiz-main.zip` 을 오른쪽 클릭 → **압축 풀기** → 바탕화면에 풉니다.
   그러면 바탕화면에 `quiz-main` 폴더가 생깁니다. 안에 `app.py`, `quiz.py`, `desktop_app.py` 가 있으면 맞습니다.

## 3. 명령 프롬프트를 그 폴더에서 열기
1. `quiz-main` 폴더를 엽니다.
2. 위쪽 **주소창**(경로가 보이는 칸)을 클릭하고, 내용을 지운 뒤 `cmd` 라고 쓰고 엔터를 누릅니다.
3. 검은 창이 `...\Desktop\quiz-main>` 처럼 열리면 준비 끝입니다.

## 4. 실행하기 (세 가지 버전)

### 창으로 뜨는 버전 (tkinter)
```
python desktop_app.py
```
교범 디자인 창이 뜹니다. 주제를 누르고 한 문제씩 풉니다.

### 웹앱 버전 (Flask)
```
pip install flask
python app.py
```
`pip install flask` 는 처음 한 번만 하면 됩니다.
그다음 크롬을 열고 주소창에 `http://127.0.0.1:5000` 을 입력합니다.
끝낼 때는 검은 창에서 **Ctrl + C** 를 누릅니다.

### 콘솔 버전 (수업 문법만)
```
python quiz.py
```
검은 창에서 번호를 입력하며 풉니다.

## 5. exe 파일 만들기
```
pip install pyinstaller
pyinstaller --onefile --windowed desktop_app.py
```
1~2분 뒤 `quiz-main\dist` 폴더에 **desktop_app.exe** 가 생깁니다. 이 파일 하나만 복사하면 파이썬이 없는 컴퓨터에서도 실행됩니다.
- `--onefile` : 파일 하나로 묶기
- `--windowed` : 검은 콘솔 창 없이 프로그램 창만 띄우기

## 막힐 때
| 증상 | 해결 |
|---|---|
| `'python'은(는) 내부 또는 외부 명령...이 아닙니다` 또는 Microsoft Store가 열림 | 1단계에서 PATH 체크를 안 한 것. `python` 대신 `py` 로 입력해 보거나, 파이썬을 다시 설치하며 체크 |
| `'pyinstaller'은(는) ... 명령이 아닙니다` | `python -m PyInstaller --onefile --windowed desktop_app.py` |
| `ModuleNotFoundError: No module named 'flask'` | `pip install flask` 를 먼저 실행 |
| `No such file or directory` | 3단계: 명령 프롬프트가 `quiz-main` 폴더에서 열렸는지 확인 |
| exe 실행 시 "Windows의 PC 보호" 경고 | **추가 정보 → 실행** (직접 만든 exe라 서명이 없어서 뜨는 경고) |
| 웹앱이 `Address already in use` | 이전에 켠 서버가 남아 있음. 그 창에서 Ctrl + C 후 다시 실행 |
