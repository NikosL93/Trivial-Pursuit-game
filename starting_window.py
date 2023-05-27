from QuizMainMenu import *
from tkinter import *
from tkinter import messagebox


class StartingWindow:
    def __init__(self):
        self.difficulty = None
        self.fullname = None
        self.name_entry = None
        self.name_label = None

        # Δημιουργεί το παράθυρο
        self.window = Tk()
        self.window.title("Trivial")
        self.window.geometry("500x400")

        # Φορτώνει τις εικόνες του background
        self.background_image = PhotoImage(file="images/background_start4.png")
        self.input_image = PhotoImage(file="images/button_background2.png")
        self.difficulty_image = PhotoImage(file="images/button_background.png")
        self.enter_name_im = PhotoImage(file="images/enter_name.png")

        # Δημιουργεί τα γραφικά στοιχεία
        self.create_widgets()

    def create_widgets(self):
        # δημιουργεί μια ετικέτα που χρησιμοποιεί μια εικόνα φόντου ίδια με το πλάτος/ύψος του παραθύρου
        background_label = Label(self.window, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # δημιουργεί την ετικέτα "Enter Name:" με τις ανάλογες παραμέτρους
        label_enter_name = Label(self.window, text="Enter Name:", font=("Bauhaus 93", 15), fg="#FFFFFF", bg="#1F4C93",
                                 image=self.enter_name_im, compound="center")
        label_enter_name.pack(pady=10)

        # δημιουργεί το πεδίο εισαγωγής ονόματος
        self.name_entry = Entry(self.window, font=("Bauhaus 93", 14))
        self.name_entry.pack()

        # δημιουργεί το submit button
        submit_button = Button(self.window, text='Submit', font=("Bauhaus 93", 14), fg="#FFFFFF", bg="#1F4C93",
                               image=self.difficulty_image, compound="center", command=self.submit_name)
        submit_button.pack(pady=5)

        # συνάρτηση για να έχει 3-D effect στα κουμπιά, σαν να πατιέται-σηκώνεται (SUNKEN-RAISED)
        def animate_button(button):
            button.config(relief="sunken")
            # χρησιμοποιώ την ανώνυμη συνάρτηση 'lambda'
            self.window.after(500, lambda: button.config(relief="raised"))

        # κάνω bind τη συνάρτηση animate_button ώστε να ενεργοποιείτε
        # όταν ο δρομέας του ποντικιού "μπει" στην περιοχή του widget 'submit_button'
        submit_button.bind("<Enter>", lambda event: animate_button(submit_button))

        # δημιουργεί το label για την επιλογή δυσκολίας 'Select Difficulty'
        label_select_difficulty = Label(self.window, text="Select Difficulty", font=("Bauhaus 93", 16), fg="#FFFFFF",
                                        bg="#1F4C93", image=self.input_image, compound="center")
        label_select_difficulty.pack(pady=5)

        # δημιουργώ τα κουμπιά - button για τα επίπεδα δυσκολίας 'easy', 'medium', 'hard' και τα τοποθετώ διαδοχικά με την pack
        easy_button = Button(self.window, text="Easy", font=("Bauhaus 93", 13), fg="#FFFFFF", bg="#377D22",
                             image=self.difficulty_image, compound="center",
                             command=lambda: self.set_difficulty("easy"))
        easy_button.pack()
        medium_button = Button(self.window, text="Medium", font=("Bauhaus 93", 13), fg="#FFFFFF", bg="#FE8B32",
                               image=self.difficulty_image, compound="center",
                               command=lambda: self.set_difficulty("medium"))
        medium_button.pack()
        hard_button = Button(self.window, text="Hard", font=("Bauhaus 93", 13), fg="#FFFFFF", bg="#FE283C",
                             image=self.difficulty_image, compound="center",
                             command=lambda: self.set_difficulty("hard"))
        hard_button.pack()

        # κάνω bind τη συνάρτηση animate_button ώστε να ενεργοποιείτε
        # όταν ο δρομέας του ποντικιού "μπει" στην περιοχή κάθε κουμπιού
        easy_button.bind("<Enter>", lambda event: animate_button(easy_button))
        medium_button.bind("<Enter>", lambda event: animate_button(medium_button))
        hard_button.bind("<Enter>", lambda event: animate_button(hard_button))

    # *** συνάρτηση για τη συμπλήρωση του ονόματος από τον χρήστη
    def submit_name(self):

        # προσωρινά αποθηκεύει το όνομα που εισήγαγε ο χρήστης, χωρίς κενά πριν-μετά
        name = self.name_entry.get().strip()

        # ελέγχει και πετάει παράθυρο προειδοποίησης εαν δεν έχει εισαχθεί όνομα
        if not name:
            messagebox.showwarning("Incomplete Information", "Please enter your name first.")
            return
        name_entry = self.name_entry.get().strip()
        # αποθηκεύει το όνομα στην ετικέτα Label που εμφανίζει μήνυμα καλωσορίσματος του χρήστη.
        self.fullname = name
        if self.name_label is None:
            self.name_label = Label(self.window, text=f"Welcome\n {self.fullname}!", font=("Bauhaus 93", 13), fg="#FFFFFF",
                                    bg="#1F4C93")
            self.name_label.place(x=65, y=150)
        else:
            self.name_label.config(text=f"Welcome\n {self.fullname}!")

        # Καθαρίζει το πεδίο εισαγωγής και το απενεργοποιεί εφόσον έχει υποβληθεί το όνομα
        self.name_entry.delete(0, END)
        self.name_entry.config(state=DISABLED)

    # *** συνάρτηση για την επιλογή του βαθμού δυσκολίας
    def set_difficulty(self, diff):
        # ελέγχω αν έχει δοθεί όνομα ,για να αφήσω να επιλέξει δυσκολία, εφόσον δεν έχει συμπληρωθεί το όνομα εμφανίζεται σχετικό παράθυρο προειδοποίησης
        if self.fullname is None:
            messagebox.showwarning("Incomplete Information", "Please enter your name first.")
            return

        # αρχικοποιώ τη δυσκολία και καλώ την συνάρτηση start_quiz για να ξεκινήσει το παιχνίδι
        self.difficulty = diff
        self.start_quiz()

    # *** συνάρτηση για να ξεκινήσει το παιχνίδι
    def start_quiz(self):
        # καλώ την μέθοδο destroy για να κλείσω το παράθυρο
        self.window.destroy()

        # Δημιουργώ αντικείμενο QuizApp από την QuizMainMenu και του στέλνω ως όρισμα το αντικείμενο game της κλάσης StartingWindow
        QuizApp(game)


# ελέγχει αν το τρέχον script εκτελείται ως το κύριο script και όχι ως ένα εισαγόμενο module
if __name__ == '__main__':
    # Δημιουργώ έμα στιγμιότυπο(game) της κλάσης StartingWindow και ξεκινάω το event loop για το παράθυρο 'window' του αντικειμένου μου.
    game = StartingWindow()
    game.window.mainloop()
