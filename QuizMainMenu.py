import requests
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox
import quiz_brain
import data
import json
import quiz_ui


class MainMenuQuizApp:
    def __init__(self, StartingWindow):
        # Main Window
        self.root = tk.Tk()
        self.root.geometry("1250x700")
        self.root.title("Quiz MainMenu Window")
        self.root.resizable(True, True)

        # Επιλογή των fonts
        self.font_style = ("BankGothic Md BT", 15)

        # Αρχικοποίηση των Frames
        self.menu_frame = ttk.Frame(self.root, style="MyFrame.TFrame")
        self.menu_frame.pack(fill="both", expand=True)
        self.topscore_frame = None
        self.question_frame = None

        self.style = ttk.Style()
        self.style.configure("MyFrame.TFrame", background="#747780")

        # Εφαρμογή του background στο MainMenu
        self.bg_image = tk.PhotoImage(file="images/pngwing.com.png")
        self.bg_label = tk.Label(self.menu_frame, image=self.bg_image, bg="#747780")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Δημιουργία πεδίου εισαγωγής ονόματος παίχτη
        self.name_label = tk.Label(self.menu_frame, bd=5, background="orange", text="Enter Your Name:",
                                   font=self.font_style)
        self.name_label.pack()
        # Μέσω της validate και validatecommand θέτουμε περιορισμούς στην εισαγωγή του ονόματος
        self.name_entry = tk.Entry(self.menu_frame, width=20, bd=7, font=self.font_style, validate="key",
                                   validatecommand=(
                                       self.root.register(self.validate_name_input), '%P'))

        # *** Εισαγωγή ονόματος παίχτη από την StartingWindow(εισαγωγή αυτής της γραμμής από Δέσποινα Μ.) ***
        self.name_entry.insert(0, StartingWindow.fullname)

        self.name_entry.pack()

        # Δημιουργία μενού για την επιλογή δυσκολίας των ερωτήσεων
        self.diff_label = tk.Label(self.menu_frame, background="orange", text="Please Choose a Difficulty Level",
                                   font=self.font_style)
        self.diff_label.pack()
        # *** Εισαγωγή difficulty από την StartingWindow (συμπλήρωση-αλλαγή αυτής της γραμμής από Δέσποινα Μ.) ***
        self.difficulty_var = tk.StringVar(value=StartingWindow.difficulty)  # Ορίζουμε τη μεταβλητή με stringvar για να μπορούμε να ανακτήσουμε την τιμή της
        self.difficulty_dropdown = ttk.Combobox(self.menu_frame, width=25, textvariable=self.difficulty_var,
                                                state="readonly",
                                                values=["easy", "medium", "hard"],
                                                font=self.font_style, style="C.TCombobox")
        self.difficulty_dropdown.pack()

        # Δημιουργία Combobox για την επιλογή κατηγορίας
        self.categories = self.get_categories()  # Κλήση της μεθόδου get_categories και ανάθεση του λεξικού με τις κατηγορίες ερωτήσεων
        self.category_var = tk.StringVar(value="General Knowledge")
        self.category_label = tk.Label(self.menu_frame, background="orange", text="Please Choose a Question Category",
                                       font=self.font_style)
        self.category_label.pack()
        self.category_options = list(
            self.categories.keys())  # Δημιουργία λίστας απο τα keys του λεξικού self.categories
        self.category_menu = ttk.Combobox(self.menu_frame, values=self.category_options, state="readonly",
                                          textvariable=self.category_var,
                                          font=self.font_style, style="C.TCombobox", width=25)
        self.category_menu.pack()
        self.custom_font = tkFont.Font(family="BankGothic Md BT", size=12)
        self.root.option_add("*TCombobox*Listbox*Font", self.custom_font)

        # Main Menu Buttons + Quit button
        self.startquiz_button = tk.Button(self.menu_frame, background="orange", text="Start Quiz !",
                                          command=self.create_question_frame, padx=70,
                                          pady=20, font=("BankGothic Md BT", 16))
        self.startquiz_button.pack(anchor="center", pady=20)
        self.topscores_button = tk.Button(self.menu_frame, background="#6fc5f3", text="Top Scores",
                                          command=self.create_topscores_frame, padx=70,
                                          pady=15, font=self.font_style)
        self.topscores_button.pack(anchor="center", pady=(100, 10))
        self.quit_button = tk.Button(self.menu_frame, text="Quit", command=self.quit_app, font=self.font_style, padx=40,
                                     pady=5,
                                     bg="#f90000")
        self.quit_button.pack(pady=10)

    # Ανάκτηση του λεξικού κατηγοριών από το API
    def get_categories(self):
        response = requests.get(url="https://opentdb.com/api_category.php")
        categories_data = response.json()[
            "trivia_categories"]  # Ανάθεση στη μεταβλητή, λίστα με τις κατηγορίες ερωτήσεων
        categories = {}  # Δημιουργία λεξικού για την καταχώρηση των κατηγοριών με key-value τα name-id
        for category_element in categories_data:
            categories[category_element["name"]] = category_element["id"]
        return categories

    # Έλεγχος για την εισαγωγή ονόματος (απαγόρευση συμβόλων και περιορισμός αριθμού χαρακτήρων)
    def validate_name_input(self, s):
        if s.isalnum() and len(s) <= 20 or s == "":
            return True
        else:
            return False

    # Μέθοδος για την επιστροφή στο κεντρικό μενού απο άλλα frames
    def return_to_mainmenu(self):
        if self.question_frame is not None:
            self.question_frame.pack_forget()
        if self.topscore_frame is not None:
            self.topscore_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    # Δημιουργία του frame των ερωτήσεων
    def create_question_frame(self):
        self.menu_frame.pack_forget()
        difficulty = self.difficulty_var.get()  # Ανάκτηση της δυσκολίας των ερωτήσεων απο το Combobox
        category = self.category_var.get()  # Ανάκτηση της κατηγορίας των ερωτήσεων απο το Combobox
        name = self.name_entry.get()  # Ανάκτηση του ονόματος του παίχτη απο Entry
        question_bank = data.get_data(difficulty, self.categories[category])
        # Έλεγχος αν το ΑΡΙ επιστρέφει ερωτήσεις
        if not question_bank:
            messagebox.showerror("No Questions !",
                                 "No TRUE - FALSE questions available for this category. Please choose another category.")
            self.return_to_mainmenu()
            return
        quiz = quiz_brain.QuizBrain(question_bank)  # Ανάθεση στη μεταβλητή την κλάση Quizbrain
        quiz_ui.QuizInterface(quiz, self, difficulty, self.categories[category], name)  # σύνδεση με quiz_ui.py

    def create_topscores_frame(self):
        self.menu_frame.pack_forget()
        self.topscore_frame = ttk.Frame(self.root, style="MyFrame.TFrame")
        self.bg_image2 = tk.PhotoImage(file="images/scores_bg.png")
        self.bg_label2 = tk.Label(self.topscore_frame, image=self.bg_image2, bg="#747780")
        self.bg_label2.place(x=0, y=0, relwidth=1, relheight=1)
        self.topscore_frame.pack(fill="both", expand=True)
        self.topscores_label = tk.Label(self.topscore_frame, background="#6fc5f3", text="TOP SCORES",
                                        font=("BankGothic Md BT", 25))
        self.topscores_label.pack(pady=10)
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
                data_items = scores.items()  # το μετατρέπω σε list από tuples key-value
                sorted_data_items = sorted(data_items, key=lambda x: x[1], reverse=True)  # με το key και το x: x[1]
                # παίρνει το 2ο στοιχείο του tuple (το score) σαν παράμετρο για να ταξινομήσει και με το reverse το κάνει σε αύξουσα σειρά
                sorted_scores = {}
                for name, score in sorted_data_items:  # κάνει unpack τo tuple kαι το μετατρέπω σε dict πάλι
                    sorted_scores[name] = score
                data = ""
                max_entries = 10  # Ο μέγιστος αριθμός των ονομάτων στον πίνακα Top Scores
                for i, (name, score) in enumerate(sorted_scores.items(), start=1):  # Η enumerate ξεκινάει από 1
                    if i > max_entries:
                        break
                    data += "{:<2}{:<22}{:>2}\n".format(str(i) + ".", name, score)
                scores_lbl = tk.Label(self.topscore_frame, text=data, font=("Consolas", 20), bg="#6fc5f3", pady=0)
                scores_lbl.pack(pady=(0, 10))
        except Exception as e:
            print(e)
        self.topscores_button = tk.Button(self.topscore_frame, text="Go To Main Menu", font=self.font_style,
                                          command=self.return_to_mainmenu, padx=70, pady=20, bg="#ccd9de")
        self.topscores_button.pack(pady=(20, 1))

    def quit_app(self):  # Μέθοδος τερματισμού της εφαρμογής (quit button command)
        self.root.destroy()


if __name__ == "__main__":
    app = MainMenuQuizApp()
    app.root.mainloop()
