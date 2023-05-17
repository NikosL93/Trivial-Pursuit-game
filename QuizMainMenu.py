import requests
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox
import quiz_brain
import data
import json
import quiz_ui


class QuizApp:
    def __init__(self):
        # Main Window
        self.root = tk.Tk()
        self.root.geometry("950x750")
        self.root.title("Quiz Start Window")
        self.root.resizable(True, True)
        # Επιλογή των fonts
        self.font_style = ("BankGothic Md BT", 15)

        # Αρχικοποίηση Frames
        self.menu_frame = ttk.Frame(self.root, style="MyFrame.TFrame")
        self.menu_frame.pack(fill="both", expand=True)
        self.topscore_frame = None
        self.question_frame = None

        self.style = ttk.Style()
        self.style.configure("MyFrame.TFrame", background="#747780")

        # Εφαρμογή του background
        self.bg_image = tk.PhotoImage(file="images/pngwing.com.png")
        self.bg_label = tk.Label(self.menu_frame, image=self.bg_image, bg="#747780")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Δημιουργία εισαγωγής ονόματος
        self.name_label = tk.Label(self.menu_frame, bd=5, background="orange", text="Enter Your Name:",
                                   font=self.font_style)
        self.name_label.pack()
        self.name_entry = tk.Entry(self.menu_frame, width=20, bd=5, font=self.font_style, validate="key",
                                   validatecommand=(
                                       self.root.register(self.validate_name_input), '%S'))
        self.name_entry.pack()
        self.scores = {}

        # Δημιουργία μενού για την επιλογή δυσκολίας
        self.diff_label = tk.Label(self.menu_frame, background="orange", text="Please Choose a Difficulty Level",
                                   font=self.font_style)
        self.diff_label.pack()
        self.difficulty_var = tk.StringVar(value="easy")
        self.difficulty_dropdown = ttk.Combobox(self.menu_frame, width=25, textvariable=self.difficulty_var,
                                                state="readonly",
                                                values=["easy", "medium", "hard"],
                                                font=self.font_style, style="C.TCombobox")
        self.difficulty_dropdown.pack()

        # Δημιουργία Combobox για την επιλογή κατηγορίας
        self.categories = self.get_categories()
        self.category_var = tk.StringVar(value="General Knowledge")
        self.category_label = tk.Label(self.menu_frame, background="orange", text="Please Choose a Question Category",
                                       font=self.font_style)
        self.category_label.pack()
        self.category_options = list(self.categories.keys())
        self.category_menu = ttk.Combobox(self.menu_frame, values=self.category_options, state="readonly",
                                          textvariable=self.category_var,
                                          font=self.font_style, style="C.TCombobox", width=25)
        self.category_menu.pack()
        self.custom_font = tkFont.Font(family="BankGothic Md BT", size=12)
        self.root.option_add("*TCombobox*Listbox*Font", self.custom_font)

        # Main Menu Buttons
        self.startquiz_button = tk.Button(self.menu_frame, background="orange", text="Start Quiz !",
                                          command=self.create_question_frame, padx=70,
                                          pady=20, font=("BankGothic Md BT", 16))
        self.startquiz_button.pack(anchor="center", pady=20)
        self.topscores_button = tk.Button(self.menu_frame, background="#6fc5f3", text="Top Scores",
                                          command=self.create_topscores_frame, padx=70,
                                          pady=15, font=self.font_style)
        self.topscores_button.pack(anchor="center", pady=(5, 200), side=tk.BOTTOM)

    # Ανάκτηση του λεξικού κατηγοριών από το API
    def get_categories(self):
        response = requests.get(url="https://opentdb.com/api_category.php")
        categories_data = response.json()["trivia_categories"]
        categories = {}
        for category_element in categories_data:
            categories[category_element["name"]] = category_element["id"]
        return categories

    def validate_name_input(self, s):
        if s.isalnum():
            return True
        else:
            return False

    def return_to_mainmenu(self):
        if self.question_frame is not None:
            self.question_frame.pack_forget()
        if self.topscore_frame is not None:
            self.topscore_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    def create_question_frame(self):
        self.menu_frame.pack_forget()
        difficulty = self.difficulty_var.get()
        category = self.category_var.get()
        name = self.name_entry.get()
        question_bank = data.get_data(difficulty, self.categories[category])
        # Έλεγχος αν το ΑΡΙ επιστρέφει ερωτήσεις
        if not question_bank:
            messagebox.showerror("No Questions !",
                                 "No TRUE - FALSE questions available for this category. Please choose another category.")
            self.return_to_mainmenu()
            return
        quiz = quiz_brain.QuizBrain(question_bank)
        quiz_ui.QuizInterface(quiz, self, difficulty, self.categories[category], name)  # συνδεση με quiz_ui.py

    def create_topscores_frame(self):
        self.menu_frame.pack_forget()
        self.topscore_frame = ttk.Frame(self.root, style="MyFrame.TFrame")
        self.bg_image2 = tk.PhotoImage(file="images/scores_bg.png")
        self.bg_label2 = tk.Label(self.topscore_frame, image=self.bg_image2, bg="#747780")
        self.bg_label2.place(x=0, y=0, relwidth=1, relheight=1)
        self.topscore_frame.pack(fill="both", expand=True)
        self.topscores_label = tk.Label(self.topscore_frame, background="orange", text="TOP SCORES",
                                        font=("BankGothic Md BT", 25))
        self.topscores_label.pack(pady=5)
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
                data_items = scores.items()  # το μετατρέπω σε list από tuples key-value
                sorted_data_items = sorted(data_items, key=lambda x: x[1], reverse=True)  # #με το key και το x: x[1]
                # παίρνει το 2ο στοιχείο του tuple το score δηλαδή σαν παράμετρο για να ταξινομήσει και με το reverse το κανει σε φθίνουσα σειρά
                sorted_scores = {}
                for name, score in sorted_data_items:  # κάνει unpack τo tuple kαι το μετατρέπω σε dict πάλι
                    sorted_scores[name] = score
                data = ""
                max_entries = 10
                for i, (name, score) in enumerate(sorted_scores.items(), 1):  # Η enumerate ξεκινάει από 1
                    if i > max_entries:
                        break
                    data += "{:<2}{:<20}{:<2}\n".format(str(i) + ".", name, score)
                scores_lbl = tk.Label(self.topscore_frame, text=data, font=("Consolas", 20), bg="#6fc5f3", pady=1)
                scores_lbl.pack(pady=(20, 10))
        except Exception as e:
            print(e)
        self.topscores_button = tk.Button(self.topscore_frame, text="Go To Main Menu", font=self.font_style,
                                          command=self.return_to_mainmenu, padx=70, pady=20, bg="#ccd9de")
        self.topscores_button.pack(pady=(20, 1))


if __name__ == "__main__":
    app = QuizApp()
    app.root.mainloop()
