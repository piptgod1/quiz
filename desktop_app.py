# 창으로 뜨는 퀴즈 프로그램 (tkinter 사용: 수업 범위 밖이라 이 파일에만 씀)
# 실행: python desktop_app.py
# exe 만들기 (Windows): pip install pyinstaller  →  pyinstaller --onefile --windowed desktop_app.py

import tkinter as tk
from quiz import get_topics, get_questions, grade, get_grade, get_advice

# 디자인: 웹앱의 교범 문서 스타일(static/style.css)과 같은 색
PAPER = "#e6e8dc"   # 바탕
SHEET = "#f2f3ec"   # 문서 카드
INK = "#22261b"     # 글자
OLIVE = "#4b5320"   # 포인트
RULE = "#a7ad8f"    # 선
STAMP = "#a3271f"   # 도장, 오답

TITLE_FONT = ("Malgun Gothic", 22, "bold")
BIG_FONT = ("Malgun Gothic", 36, "bold")
BODY_FONT = ("Malgun Gothic", 11)
BOLD_FONT = ("Malgun Gothic", 11, "bold")
SMALL_FONT = ("Malgun Gothic", 9)
CODE_FONT = ("Consolas", 11)

CHOICE_MARKS = ["가", "나", "다", "라"]


def make_window():
    """창과 머리글을 만들고, 화면 정보를 담은 딕셔너리를 돌려준다."""
    root = tk.Tk()
    root.title("파이썬 함정 퀴즈")
    root.geometry("720x680")
    root.configure(bg=PAPER)

    header = tk.Frame(root, bg=PAPER)
    header.pack(fill="x", padx=20, pady=(14, 8))
    tk.Label(header, text="파이썬 함정 퀴즈", font=("Malgun Gothic", 15, "bold"), bg=PAPER, fg=INK).pack(side="left")
    tk.Label(header, text="교육용 · 프로그래밍 교범 PY-101", font=SMALL_FONT, bg=PAPER, fg=OLIVE).pack(side="right")

    # 이중선 (교범 문서 머리글)
    tk.Frame(root, bg=INK, height=1).pack(fill="x")
    tk.Frame(root, bg=PAPER, height=2).pack(fill="x")
    tk.Frame(root, bg=INK, height=1).pack(fill="x")

    body = tk.Frame(root, bg=PAPER)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    return {"root": root, "body": body, "topic": "", "questions": [], "answers": [], "index": 0}


def clear(app):
    """본문에 있던 위젯을 모두 지운다 (화면 바꾸기)."""
    for widget in app["body"].winfo_children():
        widget.destroy()


def make_title(app, text):
    """'제1장  제목' 형태의 큰 제목."""
    row = tk.Frame(app["body"], bg=PAPER)
    row.pack(anchor="w", pady=(0, 14))
    tk.Label(row, text="제1장", font=TITLE_FONT, bg=PAPER, fg=OLIVE).pack(side="left")
    tk.Label(row, text=" " + text, font=TITLE_FONT, bg=PAPER, fg=INK).pack(side="left")


def make_button(parent, text, command, filled):
    """올리브색 버튼(filled=True) 또는 테두리 버튼."""
    if filled:
        return tk.Button(parent, text=text, command=command, font=BOLD_FONT, bg=OLIVE, fg=SHEET,
                         activebackground=INK, activeforeground=SHEET, relief="flat", padx=22, pady=8, cursor="hand2")
    return tk.Button(parent, text=text, command=command, font=BOLD_FONT, bg=PAPER, fg=OLIVE,
                     activebackground=SHEET, activeforeground=OLIVE, relief="solid", bd=1, padx=22, pady=7, cursor="hand2")


def on_topic(app, topic):
    """버튼을 눌렀을 때 실행할 함수를 만들어 돌려준다 (주제마다 하나씩)."""
    return lambda: start_quiz(app, topic)


def show_home(app):
    """첫 화면: 주제 고르기."""
    clear(app)
    make_title(app, "어떤 주제를 풀어볼까요?")
    grid = tk.Frame(app["body"], bg=PAPER)
    grid.pack(fill="x")
    grid.columnconfigure(0, weight=1, uniform="col")
    grid.columnconfigure(1, weight=1, uniform="col")

    topics = ["전체"] + get_topics()
    for i in range(len(topics)):
        topic = topics[i]
        cell = tk.Frame(grid, bg=PAPER)
        cell.grid(row=i // 2, column=i % 2, sticky="ew", padx=(0, 24) if i % 2 == 0 else 0)
        line = tk.Frame(cell, bg=PAPER)
        line.pack(fill="x")
        tk.Button(line, text=topic, command=on_topic(app, topic), font=BOLD_FONT, bg=PAPER, fg=INK,
                  activebackground=PAPER, activeforeground=STAMP, relief="flat", bd=0, highlightthickness=0, anchor="w",
                  cursor="hand2").pack(side="left", pady=8)
        count = len(get_questions(topic))
        tk.Label(line, text=f"{count}문제", font=BODY_FONT, bg=PAPER, fg=OLIVE).pack(side="right")
        tk.Frame(cell, bg=RULE, height=1).pack(fill="x")


def start_quiz(app, topic):
    """주제를 정하고 첫 문제부터 시작한다."""
    app["topic"] = topic
    app["questions"] = get_questions(topic)
    app["answers"] = []
    app["index"] = 0
    show_question(app)


def make_card(parent):
    """테두리가 있는 문서 카드."""
    card = tk.Frame(parent, bg=SHEET, highlightthickness=1, highlightbackground=RULE)
    card.pack(fill="x", pady=(0, 14))
    inner = tk.Frame(card, bg=SHEET)
    inner.pack(fill="x", padx=18, pady=14)
    return inner


def show_question(app):
    """문제 화면: 한 번에 한 문제씩."""
    clear(app)
    questions = app["questions"]
    i = app["index"]
    q = questions[i]

    make_title(app, app["topic"])
    card = make_card(app["body"])
    tk.Label(card, text=f"1-{i + 1}   {q['topic']}   ({i + 1} / {len(questions)})",
             font=SMALL_FONT, bg=SHEET, fg=OLIVE).pack(anchor="w")
    tk.Label(card, text=q["question"], font=BOLD_FONT, bg=SHEET, fg=INK,
             wraplength=600, justify="left").pack(anchor="w", pady=(4, 10))
    tk.Label(card, text=q["code"], font=CODE_FONT, bg=PAPER, fg=INK, justify="left",
             anchor="w", padx=12, pady=10).pack(fill="x", pady=(0, 10))

    choice = tk.StringVar(value="")
    for j in range(len(q["choices"])):
        tk.Radiobutton(card, text=f"{CHOICE_MARKS[j]}.  {q['choices'][j]}", variable=choice, value=str(j + 1),
                       font=BODY_FONT, bg=SHEET, fg=INK, activebackground=SHEET, selectcolor=SHEET,
                       bd=0, highlightthickness=0, anchor="w", cursor="hand2").pack(anchor="w", pady=1)

    message = tk.Label(app["body"], text="", font=BODY_FONT, bg=PAPER, fg=STAMP)
    message.pack(anchor="w")
    if i == len(questions) - 1:
        label = "채점하기"
    else:
        label = "다음 문제"
    make_button(app["body"], label, lambda: next_question(app, choice, message), True).pack(anchor="w", pady=6)


def next_question(app, choice, message):
    """고른 답을 저장하고 다음 문제 또는 결과로 넘어간다."""
    answer = choice.get()
    if answer == "":
        message.config(text="보기를 하나 골라 주세요.")
        return
    app["answers"].append(answer)
    app["index"] = app["index"] + 1
    if app["index"] < len(app["questions"]):
        show_question(app)
    else:
        show_result(app)


def show_result(app):
    """채점 화면: 점수, 등급, 복습 조언, 틀린 문제 해설."""
    clear(app)
    questions = app["questions"]
    correct, wrong = grade(questions, app["answers"])
    score = correct * 100 // len(questions)

    score_box = tk.Frame(app["body"], bg=SHEET, highlightthickness=1, highlightbackground=RULE)
    score_box.pack(fill="x", pady=(0, 14))
    inner = tk.Frame(score_box, bg=SHEET)
    inner.pack(fill="x", padx=18, pady=14)
    tk.Label(inner, text=f"{score}점", font=BIG_FONT, bg=SHEET, fg=INK).pack(anchor="w")
    tk.Label(inner, text=f"{correct} / {len(questions)} 정답 · 등급 {get_grade(score)}",
             font=BODY_FONT, bg=SHEET, fg=INK).pack(anchor="w")
    tk.Frame(inner, bg=RULE, height=1).pack(fill="x", pady=8)
    tk.Label(inner, text=get_advice(wrong), font=BODY_FONT, bg=SHEET, fg=INK,
             wraplength=600, justify="left").pack(anchor="w")
    tk.Label(score_box, text="평가 완료", font=("Malgun Gothic", 14, "bold"), bg=SHEET, fg=STAMP,
             highlightthickness=3, highlightbackground=STAMP, padx=8, pady=2).place(relx=1.0, x=-18, y=18, anchor="ne")

    buttons = tk.Frame(app["body"], bg=PAPER)
    buttons.pack(side="bottom", anchor="w", pady=(10, 0))
    make_button(buttons, "다시 풀기", on_topic(app, app["topic"]), True).pack(side="left", padx=(0, 8))
    make_button(buttons, "주제 고르기", lambda: show_home(app), False).pack(side="left")

    if len(wrong) > 0:
        show_wrong_list(app, wrong)


def show_wrong_list(app, wrong):
    """틀린 문제 해설을 스크롤되는 글상자에 보여 준다."""
    box = tk.Frame(app["body"], bg=SHEET, highlightthickness=1, highlightbackground=STAMP)
    box.pack(fill="both", expand=True)
    scroll = tk.Scrollbar(box)
    scroll.pack(side="right", fill="y")
    text = tk.Text(box, font=BODY_FONT, bg=SHEET, fg=INK, relief="flat", wrap="word",
                   padx=16, pady=12, yscrollcommand=scroll.set)
    text.pack(side="left", fill="both", expand=True)
    scroll.config(command=text.yview)

    text.tag_config("tag", font=SMALL_FONT, foreground=OLIVE)
    text.tag_config("question", font=BOLD_FONT)
    text.tag_config("code", font=CODE_FONT, background=PAPER, lmargin1=10, lmargin2=10)
    text.tag_config("answer", font=BOLD_FONT, foreground=OLIVE)

    for q in wrong:
        right = q["choices"][q["answer"] - 1]
        text.insert("end", f"{q['topic']}  ✕ 오답\n", "tag")
        text.insert("end", q["question"] + "\n", "question")
        text.insert("end", q["code"] + "\n", "code")
        text.insert("end", f"정답: {right}\n", "answer")
        text.insert("end", q["explain"] + "\n\n")
    text.config(state="disabled")


def main():
    app = make_window()
    show_home(app)
    app["root"].mainloop()


if __name__ == "__main__":
    main()
