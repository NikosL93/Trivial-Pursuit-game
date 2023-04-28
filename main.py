from data import get_data
from quiz_brain import QuizBrain
from quiz_ui import QuizInterface

# quiz initialize
def start_quiz(tk_root, difficulty, category, name):
    question_bank = get_data(difficulty, category)
    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz, difficulty, category, tk_root, name)

