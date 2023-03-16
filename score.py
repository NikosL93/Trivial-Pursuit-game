
def calculate_question_score(answer,difficulty,time):
    if difficulty.lower()=='easy':
        difficulty=1
    elif difficulty.lower()=='medium':
        difficulty=2
    else:
        difficulty=3
    return answer*difficulty*time
