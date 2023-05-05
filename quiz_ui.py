from tkinter import *
from quiz_brain import QuizBrain
from data import get_data
from tkinter import messagebox
import json

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain, quizapp, difficulty, category, name):
        #τα κανω property με το self γτ θελω να τα χρησιμοποιω σ ολη τη κλασση ενω το false_button κανονική μεταβλητη.
        self.quizapp = quizapp
        self.name = name
        self.difficulty = difficulty
        self.category = category
        self.quiz = quiz_brain
        self.round_score = 0
        self.total_score = 0
        self.rounds = 0 # σύνολο γύρων
        self.prev_round_questions_unanswered = 0
        self.curr_round_questions_unanswered = 0
        self.window = Frame(quizapp.root, bg="#747780")
        self.window.pack(fill=BOTH, expand=True)

        self.main_menu = Button(self.window, text="Main Menu", command=self.return_to_main_menu, font=quizapp.font_style)
        self.main_menu.pack(side=TOP,  pady=5)

        self.canvas = Canvas(self.window, width=600, height=500, bg="#777480")
        bg = PhotoImage(file="images/pngwing.com.png")
        self.canvas.create_image(0, 0, image=bg, anchor="nw")
        self.question_text = self.canvas.create_text(
            300,
            410,
            width=500,
            text="Some Question Text",
            font=("Arial", 20, "italic",)
        )
        self.canvas.pack(side=TOP, pady=30)

        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(self.window, image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.pack(side=LEFT, padx=10)

        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(self.window, image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.pack(side=RIGHT, padx=10)

        prev_image = PhotoImage(file="images/back.png")
        self.prev_button = Button(self.window, image=prev_image, highlightthickness=0, command=self.get_prev_question)
        self.prev_button.pack(side=LEFT, padx=100)

        next_image = PhotoImage(file="images/next.png")
        self.next_button = Button(self.window, image=next_image, bg="BLACK", highlightthickness=0,
                                  command=self.get_next_question)
        self.next_button.pack(side=RIGHT, padx=100)



        if self.quiz.still_has_questions():
            self.get_next_question()
        self.window.mainloop()

    def return_to_main_menu(self):
        self.window.pack_forget()
        self.quizapp.menu_frame.pack(side="top", fill="both", expand=True)

    def calculate_round_score(self):
        for q in range(9):
            self.round_score += self.quiz.calculate_question_score(self.quiz.questions_score[q], self.difficulty, 1)

    def calculate_total_score(self):
        self.total_score += self.round_score
        try:
            with open("scores", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}  # σε περιπτωση που δεν υπαρχει το αρχειο δημιουργει ενα κενο dict
        data[self.name] = self.total_score
        with open("scores", "w") as file:
            json.dump(data, file)
    def gameover(self):
        self.calculate_round_score()
        self.calculate_total_score()
        messagebox.showinfo("Information",
                            f"Game-over!\nRound score: {self.round_score}\nTotal score: {self.total_score}")
        self.canvas.itemconfig(self.question_text, text="Game-over!")
        self.window.after(100, self.yes_button.destroy)
        self.window.after(100, self.no_button.destroy)
        self.window.after(100, self.false_button.destroy)
        self.window.after(100, self.true_button.destroy)
        self.window.after(100, self.prev_button.destroy)
        self.window.after(100, self.next_button.destroy)
        return 0
    def new_round(self):
        # Υπολογισμός συνολικού σκορ σε κάθε καινούργιο γύρο και συνολικού σκορ
        self.calculate_round_score()
        self.calculate_total_score()
        # έλεγχος αν υπάρχουν >3 ερωτήσεις μη απαντημένες σε 2 συνεχόμενους γύρους σε κάθε γύρο
        self.rounds += 1
        if self.rounds == 1: #αρχικη περίπτωση 1ου γυρου
            for q in range(9):
                if self.quiz.questions_answered[q] == 0: self.prev_round_questions_unanswered += 1
        else:
            for q in range(9): #περιπτωση 1+ γύρων
                if self.quiz.questions_answered[q] == 0 : self.curr_round_questions_unanswered += 1
            if self.prev_round_questions_unanswered > 3 and self.curr_round_questions_unanswered > 3: #game-over
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
        question_bank = get_data(self.difficulty,self.category)
        self.quiz = QuizBrain(question_bank)
        self.window.after(1000, self.get_next_question)

    def get_next_question(self):
        try:#αν υπαρχουν τα yes,no buttons
            self.window.after(0, self.yes_button.destroy)
            self.window.after(0, self.no_button.destroy)
        except: pass
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.true_button['state'] = 'active' #μετα την εμφανιση της επομενης ερωτησης τα buttons γινονται active
            self.false_button['state'] = 'active'
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz. Another round?")
            self.yes_button = Button(self.canvas, text="YES", command=self.new_round)
            self.yes_button.place(x=200, y=450)
            self.no_button = Button(self.canvas, text="NO", command=self.gameover)
            self.no_button.place(x=350, y=450)

    def get_prev_question(self):
        try:#αν υπαρχουν τα yes,no buttons
            self.window.after(0, self.yes_button.destroy)
            self.window.after(0, self.no_button.destroy)
        except: pass
        if self.quiz.question_number > 0:
            q_text = self.quiz.prev_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.true_button['state'] = 'active'
            self.false_button['state'] = 'active'

    def true_pressed(self):
        self.quiz.check_answer("True")
        self.true_button['state'] = 'disabled'
        self.window.after(1000, self.get_next_question)
    def false_pressed(self):
        self.quiz.check_answer("False")
        self.false_button['state'] = 'disabled'
        self.window.after(1000, self.get_next_question)








