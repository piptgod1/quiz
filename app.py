# 웹 화면 (Flask 사용: 수업 범위 밖이라 이 파일에만 씀)
# 실행: pip install flask  →  python app.py  →  브라우저에서 http://127.0.0.1:5000
# 휴대폰: 같은 Wi-Fi에서 http://(PC의 IP 주소):5000

from html import escape
from flask import Flask, request
from quiz import get_topics, get_questions, grade, get_grade, get_advice

app = Flask(__name__)



def page(title, body):
    """모든 화면에 공통으로 쓰는 HTML 틀."""
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header><a href="/">파이썬 함정 퀴즈</a></header>
<main>{body}</main>
</body>
</html>"""


@app.route("/")
def home():
    """첫 화면: 주제 고르기."""
    body = "<h1>어떤 주제를 풀어볼까요?</h1>\n<div class='topics'>"
    for topic in ["전체"] + get_topics():
        count = len(get_questions(topic))
        body = body + f"<a class='topic' href='/quiz?topic={topic}'>{topic}<span>{count}문제</span></a>"
    body = body + "</div>"
    return page("파이썬 함정 퀴즈", body)


@app.route("/quiz")
def quiz():
    """문제 화면: 고른 주제의 문제를 한 번에 보여준다."""
    topic = request.args.get("topic", "전체")
    questions = get_questions(topic)
    body = f"<h1>{topic}</h1>\n<form method='post' action='/result'>"
    body = body + f"<input type='hidden' name='topic' value='{topic}'>"
    for i in range(len(questions)):
        q = questions[i]
        body = body + f"<section class='card'><p class='tag'>{q['topic']}</p>"
        body = body + f"<h2>{i + 1}. {escape(q['question'])}</h2>"
        body = body + f"<pre>{escape(q['code'])}</pre>"
        for j in range(len(q["choices"])):
            body = body + f"<label class='choice'><input type='radio' name='q{i}' value='{j + 1}' required> {escape(q['choices'][j])}</label>"
        body = body + "</section>"
    body = body + "<button type='submit'>채점하기</button></form>"
    return page(topic + " 문제", body)


@app.route("/result", methods=["POST"])
def result():
    """채점 화면: 점수, 등급, 틀린 문제 해설, 복습 조언."""
    topic = request.form.get("topic", "전체")
    questions = get_questions(topic)
    answers = []
    for i in range(len(questions)):
        answers.append(request.form.get(f"q{i}", ""))
    correct, wrong = grade(questions, answers)
    score = correct * 100 // len(questions)

    body = "<section class='score'>"
    body = body + f"<p class='big'>{score}점</p><p>{correct} / {len(questions)} 정답 · 등급 {get_grade(score)}</p>"
    body = body + f"<p class='advice'>{escape(get_advice(wrong))}</p></section>"
    for q in wrong:
        right = q["choices"][q["answer"] - 1]
        body = body + f"<section class='card wrong'><p class='tag'>{q['topic']}</p>"
        body = body + f"<h2>{escape(q['question'])}</h2><pre>{escape(q['code'])}</pre>"
        body = body + f"<p class='answer'>정답: {escape(right)}</p><p>{escape(q['explain'])}</p></section>"
    body = body + f"<a class='button' href='/quiz?topic={topic}'>다시 풀기</a> <a class='button ghost' href='/'>주제 고르기</a>"
    return page("채점 결과", body)


def main():
    # host="0.0.0.0": 같은 Wi-Fi에 있는 휴대폰에서도 접속할 수 있게 연다
    # debug는 끈다 (켜 두면 같은 네트워크의 다른 사람이 서버를 조작할 수 있음)
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
