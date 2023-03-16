from data import get_data
from quiz_brain import QuizBrain
from ui import QuizInterface
from tkinter import *

difficulty = None
fullname = None
# quiz initialize
def start_quiz():
    window.destroy()
    question_bank = get_data(difficulty)
    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz, difficulty)
#ui
def submit_name():
    global fullname
    fullname = name.get()
    Label(text="Name submitted!").pack(pady=10)
def set_difficulty(diff):
    global difficulty
    difficulty = diff

window = Tk()
window.title("Trivial")
window.eval('tk::PlaceWindow . center')
window.geometry('300x500')
Label(text="Enter Name").pack()
name = Entry(window)
name.pack()
Button(text='Submit', command=submit_name).pack(pady=10)
Label(text="Enter Difficulty").pack(pady=5)
Button(text="Easy", command=lambda: [set_difficulty("easy"), start_quiz()]).pack()
Button(text="Medium", command=lambda: [set_difficulty("medium"), start_quiz()]).pack()
Button(text="Hard", command=lambda: [set_difficulty("hard"), start_quiz()]).pack()

window.mainloop()
