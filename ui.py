from tkinter import *
from quiz_brain import QuizBrain
from data import get_data
from tkinter import messagebox

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain,difficulty):
        #τα κανω property με το self γτ θελω να τα χρησιμοποιω σ ολη τη κλασση ενω το false_button κανονική μεταβλητη.
        self.difficulty = difficulty
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Trivial")
        self.window.config(padx=80, pady=20, bg=THEME_COLOR)
        self.round_score = 0
        self.total_score = 0
        self.score_label = Label(text="", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)
        self.canvas = Canvas(width=600, height=500, bg="#37625C")
        bg = PhotoImage(file="images/pngwing.com.png")
        self.canvas.create_image(0,0, image=bg, anchor="nw")
        self.question_text = self.canvas.create_text(
            300,
            410,
            width=500,
            text="Some Question Text",
            font=("Arial", 20, "italic",)
        )
        self.canvas.grid(row=1, column=1, columnspan=2, pady=50) #row=1 γιατι θελω να ναι κατω απ το score π ειναι 0
        #και το pady ειναι το περιθωριο κατω απ το score

        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=3, column=0,columnspan=2)

        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=3, column=2)

        prev_image = PhotoImage(file="images/back.png")
        self.prev_button = Button(image=prev_image, highlightthickness=0, command=self.get_prev_question)
        self.prev_button.grid(row=2, column=1,sticky=E,padx=5) # to sticky=E το μετατοπιζει στο τερμα ανατολικα

        next_image = PhotoImage(file="images/next.png")
        self.next_button = Button(image=next_image, highlightthickness=0, command=self.get_next_question)
        self.next_button.grid(row=2, column=2, sticky=W)

        if self.quiz.still_has_questions():
            self.get_next_question()
        self.window.mainloop()

    def calculate_round_score(self):
        for q in range(9):
            self.round_score += self.quiz.calculate_question_score(self.quiz.questions_score[q], self.difficulty, 1)

    def new_round(self):
        self.calculate_round_score()
        self.total_score += self.round_score
        self.window.after(100, self.yes_button.destroy)
        self.window.after(100, self.no_button.destroy)
        messagebox.showinfo("Information", f"Round score: {self.round_score} \n Total score: {self.total_score}")
        self.round_score = 0
        question_bank = get_data(self.difficulty)
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
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz. Another round?")
            self.yes_button = Button(self.canvas, text="YES", command=self.new_round)
            self.yes_button.place(x=200,y=450)
            self.no_button = Button(self.canvas, text="NO", command=exit)
            self.no_button.place(x=350, y=450)

    def get_prev_question(self):
        try:#αν υπαρχουν τα yes,no buttons
            self.window.after(0, self.yes_button.destroy)
            self.window.after(0, self.no_button.destroy)
        except: pass
        if self.quiz.question_number > 0:
            q_text = self.quiz.prev_question()
            self.canvas.itemconfig(self.question_text, text=q_text)

    def true_pressed(self):
        self.quiz.check_answer("True")
        self.window.after(1000, self.get_next_question)

    def false_pressed(self):
        self.quiz.check_answer("False")
        self.window.after(1000, self.get_next_question)








