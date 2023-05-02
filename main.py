from data import get_data
from quiz_brain import QuizBrain
from quiz_ui import QuizInterface

# quiz initialize
def start_quiz(quizapp, difficulty, category, name):
    question_bank = get_data(difficulty, category)
    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz, quizapp, difficulty, category, name)

