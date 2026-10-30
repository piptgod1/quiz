# 채점과 학습 도우미 로직 (수업에서 배운 문법만 사용)
# 웹이 없어도 이 파일만 실행하면 콘솔에서 퀴즈를 풀 수 있다.

from questions import QUESTIONS


def get_topics():
    """문제에 나오는 주제 목록을 순서대로, 중복 없이 돌려준다."""
    topics = []
    for q in QUESTIONS:
        if q["topic"] not in topics:
            topics.append(q["topic"])
    return topics


def get_questions(topic):
    """주제에 맞는 문제만 골라 리스트로 돌려준다. "전체"이면 모든 문제."""
    if topic == "전체":
        return QUESTIONS
    result = []
    for q in QUESTIONS:
        if q["topic"] == topic:
            result.append(q)
    return result


def check_answer(question, user_answer):
    """사용자 답(문자열)을 정수로 바꿔 정답과 비교한다."""
    try:
        return int(user_answer) == question["answer"]
    except ValueError:
        return False


def grade(questions, answers):
    """answers: 사용자가 고른 번호(문자열) 리스트. 맞은 개수와 틀린 문제 리스트를 돌려준다."""
    correct = 0
    wrong = []
    for i in range(len(questions)):
        if check_answer(questions[i], answers[i]):
            correct = correct + 1
        else:
            wrong.append(questions[i])
    return correct, wrong


def get_grade(score):
    """100점 만점 점수를 등급으로 바꾼다 (practice_04 패턴)."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def get_advice(wrong):
    """틀린 문제의 주제를 세어서 복습할 주제를 알려준다 (학습 도우미)."""
    if len(wrong) == 0:
        return "모두 맞았어요! 시험 함정을 잘 피했습니다."
    counts = {}
    for q in wrong:
        topic = q["topic"]
        if topic in counts:
            counts[topic] = counts[topic] + 1
        else:
            counts[topic] = 1
    worst = ""
    for topic in counts:
        if worst == "" or counts[topic] > counts[worst]:
            worst = topic
    return f"'{worst}' 주제를 {counts[worst]}문제 틀렸어요. 이 부분을 먼저 복습하세요."


def get_choice(prompt, size):
    """1~size 사이 정수가 입력될 때까지 다시 묻는다."""
    while True:
        try:
            n = int(input(prompt))
        except ValueError:
            print("정수를 입력하세요")
            continue
        if 1 <= n <= size:
            return n
        print("범위를 벗어났습니다")


def main():
    questions = get_questions("전체")
    answers = []
    for i in range(len(questions)):
        q = questions[i]
        print(f"\n[{i + 1}] ({q['topic']}) {q['question']}")
        print(q["code"])
        for j in range(len(q["choices"])):
            print(f"  {j + 1}. {q['choices'][j]}")
        answers.append(str(get_choice("답 번호: ", len(q["choices"]))))
    correct, wrong = grade(questions, answers)
    score = correct * 100 // len(questions)
    print(f"\n{correct}/{len(questions)} 정답, {score}점, 등급: {get_grade(score)}")
    print(get_advice(wrong))


if __name__ == "__main__":
    main()
