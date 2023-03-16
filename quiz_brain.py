import html


class QuizBrain:

    def __init__(self, q_list):

        self.question_number = -1  # -1 γτ to next question τρεχει και στο init
        self.questions_score = {}
        for q in range(9):
            self.questions_score[q] = 0   # αρχικοποιηση λεξικού απαντήσεων (0 λαθος 1 σωστή)
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)-1

    def next_question(self):
        self.question_number += 1
        print(self.question_number)
        self.current_question = self.question_list[self.question_number]
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number+1}: {q_text}"

    def prev_question(self):
        self.question_number -= 1
        print(self.question_number)
        self.current_question = self.question_list[self.question_number]
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number+1}: {q_text}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer # παει στο data.py και παιρνει το κλειδι αnswer tου λεξικου
        if user_answer.lower() == correct_answer.lower():
            self.questions_score[self.question_number] = 1
            print("right answer")
            return True
        else:
            return False

