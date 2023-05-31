import html


class QuizBrain:

    def __init__(self, q_list):
        self.question_number = -1  # -1 γτ to next question τρέχει και στο init
        self.questions_score = {}
        self.questions_answered = {}
        for q in range(9):
            self.questions_score[q] = 0  # αρχικοποίηση λεξικού απαντήσεων (0 λάθος 1 σωστή)
            self.questions_answered[q] = 0  # αρχικοποίηση λεξικού απαντημένων ερωτήσεων (0 αναπάντητη 1 απαντημένη)
        self.question_list = q_list
        self.current_question = None

        self.user_answers = {}  # Chris. Λεξικό για την αποθήκευση των απαντήσεων και την εμφάνιση τους στην οθόνη

    def still_has_questions(self):
        return self.question_number < len(self.question_list) - 1

    def next_question(self):
        self.question_number += 1
        self.current_question = self.question_list[self.question_number]
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number + 1}: {q_text}"

    def prev_question(self):
        self.question_number -= 1
        self.current_question = self.question_list[self.question_number]
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number + 1}: {q_text}"

    def check_answer(self, user_answer):
        self.questions_answered[self.question_number] = 1  # αν απαντήθηκε η ερώτηση
        correct_answer = self.current_question.answer  # πάει στο data.py και παίρνει το κλειδί αnswer tου λεξικού (σωστή απάντηση)

        self.user_answers[self.question_number] = user_answer.lower()  # Chris. Αποθήκευση της απάντησης του χρήστη στο λεξικό user_answers

        if user_answer.lower() == correct_answer.lower():
            self.questions_score[self.question_number] = 1
            print("right answer")
            return True
        else:
            print("wrong answer")
            return False

    def calculate_question_score(self, answer, difficulty, time):
        if difficulty.lower() == 'easy':
            difficulty = 1
        elif difficulty.lower() == 'medium':
            difficulty = 2
        else:
            difficulty = 3
        if time != 0:
            time_score = 1/time
        else:
            return 0
        return answer * difficulty * time_score

    def get_answer_info(self):  # Chris. Μέθοδος που επιστέφει την εκτύπωση της απάντησης που έχει δώσει ο χρήστης
        if self.questions_answered.get(self.question_number) == 1:  # Chris. Έλεγχος αν έχει απαντηθεί η ερώτηση
            user_answer = self.user_answers.get(self.question_number)  # Chris. Ανάκτηση της απάντησης του χρήστη απο το λεξικό user_answers
            return "You answered: {}".format(user_answer.upper())
        else:
            return "You haven't answered this question yet."
