from tkinter import *
from quiz_brain import QuizBrain
from data import get_data
from tkinter import messagebox
import json
from quiz_timer import QuizTimer, Timer  # Εισαγωγή της QuizTimer και Timer class
from answer_status import AnswerInfoLabel  # Εισαγωγή της AnswerInfoLabel απο answer_status.py


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain, quizapp, difficulty, category, name):
        self.quiz = quiz_brain
        self.quizapp = quizapp
        self.difficulty = difficulty
        self.category = category
        self.name = name
        quizapp.root.title("Trivial Quiz")
        self.round_score = 0
        self.total_score = 0
        self.rounds = 0  # σύνολο γύρων
        self.prev_round_questions_unanswered = 0
        self.curr_round_questions_unanswered = 0
        self.window = Frame(quizapp.root, bg="#747780")
        self.window.pack(fill=BOTH, expand=True)

        self.main_menu = Button(self.window, text="Go to Main Menu", command=self.return_to_main_menu,
                                font=quizapp.font_style, padx=70, bg="#ccd9de")
        self.main_menu.pack(side=TOP, pady=2)

        self.canvas = Canvas(self.window, width=600, height=500, bg="#777480")
        bg = PhotoImage(file="images/quiz_bg.png")
        self.canvas.create_image(0, 0, image=bg, anchor="nw")
        self.question_text = self.canvas.create_text(
            300,
            410,
            width=500,
            text="Some Question Text",
            font=("Arial", 20, "italic")
        )
        self.canvas.pack(side=TOP, pady=10)

        true_image = PhotoImage(file="images/True.png")
        self.true_button = Button(self.window, image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.pack(side=LEFT, padx=10, pady=5)

        false_image = PhotoImage(file="images/False.png")
        self.false_button = Button(self.window, image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.pack(side=RIGHT, padx=10, pady=5)

        prev_image = PhotoImage(file="images/back.png")
        self.prev_button = Button(self.window, image=prev_image, highlightthickness=0, command=self.get_prev_question)
        self.prev_button.pack(side=LEFT, padx=(100, 5))

        next_image = PhotoImage(file="images/next.png")
        self.next_button = Button(self.window, image=next_image, highlightthickness=0,
                                  command=self.get_next_question)
        self.next_button.pack(side=RIGHT, padx=(5, 100))

        # Chris l.61-65 (εισαγωγή του AnswerInfoLabel και των timers)
        self.answer_info_label = AnswerInfoLabel(self.window)  # Chris. Δημιουργία instance της AnswerInfoLabel
        self.quiz_timer = QuizTimer(self.window,
                                    self.gameover)  # Chris. Initialize της QuizTimer class στην μεταβλητή quiz_timer
        self.question_timer = Timer()  # Chris. Αντικείμενο της κλάσης Timer (αφορά το timer της κάθε ερώτησης)
        self.question_time_dict = {}  # Chris. Λεξικό αποθήκευσης του χρόνου απάντησης κάθε ερώτησης

        if self.quiz.still_has_questions():
            self.get_next_question()
        self.window.mainloop()

    def return_to_main_menu(self):
        self.quiz_timer.stop_timer()  # Chris. Τερματισμός του timer του γύρου ερωτήσεων
        self.window.pack_forget()
        self.quizapp.root.title("Quiz MainMenu Window")
        self.quizapp.menu_frame.pack(side="top", fill="both", expand=True)

    def calculate_round_score(self):
        for q in range(9):
            time_spent = self.question_time_dict.get(q, 0)  # Chris. Ανάκτηση του χρόνου απάντησης της κάθε ερώτησης απο το λεξικό (αν δε βρεθεί επιστρέφει 0)
            self.round_score += self.quiz.calculate_question_score(self.quiz.questions_score[q], self.difficulty,
                                                                   time_spent)
        remaining_time = self.quiz_timer.get_remaining_time()  # Chris. Ανάκτηση του εναπομείναντα χρόνου όλου του γύρου σε sec
        if remaining_time > 0:
            self.round_score *= remaining_time  # Chris. Εάν ο χρόνος που απομένει είναι μεγαλύτερος απο 0, πολλαπλασιάζεται με το round_score ως επιβράβευση
        self.round_score = int(self.round_score)  # Chris. Στρογγυλοποίηση του αποτελέσματος σε integer

    def calculate_total_score(self):
        self.total_score += self.round_score
        try:
            with open("scores.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}  # Σε περίπτωση που δεν υπάρχει το αρχείο δημιουργεί ενα κενό dict
        if self.name not in data or self.total_score > data[self.name]:
            data[self.name] = self.total_score
        with open("scores.json", "w") as file:
            json.dump(data, file)

        print(f"Total Score: {self.total_score}")
        print(f"Max Score in data: {max(data.values(), default=0)}")
        # Chris. Έλεγχος και εμφάνιση μηνύματος σε περίπτωση που ο χρήστης πέτυχε την υψηλότερη βαθμολογία
        if self.total_score >= max(data.values(), default=0) and self.total_score != 0:
            messagebox.showinfo("Συγχαρητήρια!\n", "Έχεις πετύχει την υψηλότερη βαθμολογία!")

    def gameover(self):
        self.calculate_round_score()
        self.quiz_timer.stop_timer()  # Chris. Τερματισμός του timer του γύρου ερωτήσεων
        self.calculate_total_score()
        messagebox.showinfo("Information",
                            f"Game-over!\nRound score: {self.round_score}\nTotal score: {self.total_score}")
        self.canvas.itemconfig(self.question_text, text="Game-over!")
        try:
            self.window.after(100, self.yes_button.destroy)
            self.window.after(100, self.no_button.destroy)
        except:
            pass
        self.window.after(100, self.false_button.destroy)
        self.window.after(100, self.true_button.destroy)
        self.window.after(100, self.prev_button.destroy)
        self.window.after(100, self.next_button.destroy)

        return 0

    def new_round(self):
        # Υπολογισμός συνολικού σκορ σε κάθε καινούργιο γύρο και συνολικού σκορ
        self.calculate_round_score()
        self.quiz_timer.stop_timer()  # Chris. Τερματισμός του timer του γύρου ερωτήσεων
        self.calculate_total_score()
        # έλεγχος αν υπάρχουν >3 ερωτήσεις μη απαντημένες σε 2 συνεχόμενους γύρους σε κάθε γύρο
        self.rounds += 1
        if self.rounds == 1:  # αρχική περίπτωση 1ου γύρου
            for q in range(9):
                if self.quiz.questions_answered[q] == 0: self.prev_round_questions_unanswered += 1
        else:
            for q in range(9):  # περίπτωση 1+ γύρων
                if self.quiz.questions_answered[q] == 0: self.curr_round_questions_unanswered += 1
            if self.prev_round_questions_unanswered > 3 and self.curr_round_questions_unanswered > 3:  # game-over
                messagebox.showinfo("Information",
                                    f"Game-over!\nRound score: {self.round_score}\nTotal score: {self.total_score}")
                self.window.after(100, self.yes_button.destroy)
                self.window.after(100, self.no_button.destroy)
                self.window.after(100, self.false_button.destroy)
                self.window.after(100, self.true_button.destroy)
                self.window.after(100, self.prev_button.destroy)
                self.window.after(100, self.next_button.destroy)
                self.canvas.itemconfig(self.question_text, text="Game-over!")
                return 0
            self.prev_round_questions_unanswered = self.curr_round_questions_unanswered
            self.curr_round_questions_unanswered = 0
        self.window.after(100, self.yes_button.destroy)
        self.window.after(100, self.no_button.destroy)
        messagebox.showinfo("Information", f"Round score: {self.round_score} \n Total score: {self.total_score}")
        self.round_score = 0
        question_bank = get_data(self.difficulty, self.category)
        self.quiz = QuizBrain(question_bank)
        self.quiz_timer.restart_timer()  # Chris. Επανέναρξη του timer του κάθε γύρου ερωτήσεων
        self.quiz_timer.reset_question_timer()  # Chris. Επανέναρξη του timer της κάθε ερώτησης
        self.window.after(500, self.get_next_question)

    def get_next_question(self):
        try:  # αν υπάρχουν τα yes,no buttons
            self.window.after(0, self.yes_button.destroy)
            self.window.after(0, self.no_button.destroy)
        except:
            pass
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.true_button['state'] = 'active'  # μετά την εμφάνιση της επομένης ερώτησης τα buttons γίνονται active
            self.false_button['state'] = 'active'

            answer_info = self.quiz.get_answer_info()  # Chris. Ανάκτηση της απάντησης (True ή False) απο τη μέθοδο get_answer_info του quiz_brain.py
            self.answer_info_label.update_label(answer_info)  # Chris. Κάνει update το label και το εμφανίζει στην οθόνη

            self.question_timer.start()  # Chris. Έναρξη του timer της ερώτησης
            self.quiz_timer.reset_question_timer()  # Chris. Επανέναρξη του timer της κάθε ερώτησης

        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz. Another round?")
            self.yes_button = Button(self.canvas, text="YES", padx=30, command=self.new_round)
            self.yes_button.place(x=150, y=450)
            self.no_button = Button(self.canvas, text="NO", padx=30, command=self.gameover)
            self.no_button.place(x=350, y=450)

    def get_prev_question(self):
        try:  # αν υπάρχουν τα yes,no buttons
            self.window.after(0, self.yes_button.destroy)
            self.window.after(0, self.no_button.destroy)
        except:
            pass
        if self.quiz.question_number > 0:
            q_text = self.quiz.prev_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.true_button['state'] = 'active'
            self.false_button['state'] = 'active'

            answer_info = self.quiz.get_answer_info()  # Chris. Ανάκτηση της απάντησης (True ή False) απο τη μέθοδο get_answer_info του quiz_brain.py
            self.answer_info_label.update_label(answer_info)  # Chris. Κάνει update το label για να εμφανίζεται η επιλεγμένη απάντηση στην οθόνη

            self.question_timer.start()  # Chris. Έναρξη του timer της ερώτησης
            self.quiz_timer.reset_question_timer()  # Chris. Επανέναρξη του timer της κάθε ερώτησης

    def true_pressed(self):
        self.quiz.check_answer("True")

        answer_info = self.quiz.get_answer_info()
        self.answer_info_label.update_label(answer_info)  # Chris. Κάνει update το label για να εμφανίζεται η επιλεγμένη απάντηση στην οθόνη

        elapsed_time = self.question_timer.stop()  # Chris. Ανάκτηση του χρόνου απάντησης της κάθε ερώτησης (μέθοδος stop())
        self.question_time_dict[self.quiz.question_number] = elapsed_time  # Chris. Καταχώρηση του χρόνου απάντησης της ερώτησης στο λεξικό
        self.quiz_timer.reset_question_timer()  # Chris. Επανέναρξη του timer της κάθε ερώτησης (μέθοδος reset_question_timer())

        self.true_button['state'] = 'disabled'
        self.window.after(500, self.get_next_question)

    def false_pressed(self):
        self.quiz.check_answer("False")

        answer_info = self.quiz.get_answer_info()  # Chris. Ανάκτηση της απάντησης (True ή False) απο τη μέθοδο get_answer_info του quiz_brain.py
        self.answer_info_label.update_label(answer_info)  # Chris. Κάνει update το label για να εμφανίζεται η επιλεγμένη απάντηση στην οθόνη

        elapsed_time = self.question_timer.stop()  # Chris. Ανάκτηση του χρόνου απάντησης της κάθε ερώτησης (μέθοδος stop())
        self.question_time_dict[self.quiz.question_number] = elapsed_time  # Chris. Καταχώρηση του χρόνου απάντησης της ερώτησης στο λεξικό
        self.quiz_timer.reset_question_timer()  # Chris. Επανέναρξη του timer της κάθε ερώτησης (μέθοδος reset_question_timer())

        self.false_button['state'] = 'disabled'
        self.window.after(500, self.get_next_question)
