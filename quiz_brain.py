import html


class QuizBrain:

    def __init__(self, q_list):
        self.question_number = -1  # -1 γτ to next question τρέχει και στο init
        self.questions_score = {}
        self.questions_answered = {}
        for q in range(9):
            self.questions_score[q] = 0   # αρχικοποίηση λεξικού απαντήσεων (0 λάθος 1 σωστή)
            self.questions_answered[q] = 0 # αρχικοποίηση λεξικού απαντημένων ερωτήσεων (0 αναπάντητη 1 απαντημένη)
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)-1

    def next_question(self):
        self.question_number += 1
        self.current_question = self.question_list[self.question_number]
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number+1}: {q_text}"

    def prev_question(self):
        self.question_number -= 1
        self.current_question = self.question_list[self.question_number]
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number+1}: {q_text}"

    def check_answer(self, user_answer):
        self.questions_answered[self.question_number] = 1 #αν απαντηθηκε η ερωτηση
        correct_answer = self.current_question.answer # παει στο data.py και παιρνει το κλειδι αnswer tου λεξικου(σωστήη απάντηση)
        if user_answer.lower() == correct_answer.lower():
            self.questions_score[self.question_number] = 1
            print("right answer")
            return True
        else:
            print("wrong answer")
            return False

    def calculate_question_score(self, answer, difficulty):
        if difficulty.lower() == 'easy':
            difficulty = 1
        elif difficulty.lower() == 'medium':
            difficulty = 2
        else:
            difficulty = 3
        return answer * difficulty

