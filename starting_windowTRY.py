from data import get_data
from quiz_brain import QuizBrain
from quiz_ui import QuizInterface
from tkinter import *
from tkinter import messagebox

class TrivialGame:
    def __init__(self):
        self.difficulty = None
        self.fullname = None
        self.name_entry = None
        self.name_label = None

        # Create the Tkinter window
        self.window = Tk()
        self.window.title("Trivial")
        self.window.geometry("500x400")

        # Load the background images
        self.background_image = PhotoImage(file="images/background_start4.png")
        self.input_image = PhotoImage(file="images/button_background2.png")
        self.difficulty_image = PhotoImage(file="images/button_background.png")
        self.enter_name_im = PhotoImage(file="images/enter_name.png")

        # Create the user interface
        self.create_widgets()

    def create_widgets(self):
        # Set the background image
        background_label = Label(self.window, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Create the "Enter Name" label
        label_enter_name = Label(self.window, text="Enter Name:", font=("Arial", 15), fg="#FFFFFF", bg="#1F4C93", image=self.enter_name_im, compound="center")
        label_enter_name.pack(pady=10)

        # Create the name entry field
        self.name_entry = Entry(self.window, font=("Arial", 14))
        self.name_entry.pack()

        # Create the submit button
        submit_button = Button(self.window, text='Submit', font=("Bauhaus 93", 14), fg="#FFFFFF", bg="#1F4C93", image=self.difficulty_image, compound="center", command=self.submit_name)
        submit_button.pack(pady=5)

        # Create a function to animate a button
        def animate_button(button):
            button.config(relief="sunken")
            self.window.after(500, lambda: button.config(relief="raised"))

        # Bind the animate_button function to the mouseover event of the buttons
        submit_button.bind("<Enter>", lambda event: animate_button(submit_button))

        # Create the "Select Difficulty" label
        label_select_difficulty = Label(self.window, text="Select Difficulty", font=("Bauhaus 93", 16), fg="#FFFFFF", bg="#1F4C93", image=self.input_image, compound="center")
        label_select_difficulty.pack(pady=5)

        # Create the difficulty buttons
        easy_button = Button(self.window, text="Easy", font=("Bauhaus 93", 13), fg="#FFFFFF", bg="#377D22", image=self.difficulty_image, compound="center", command=lambda: self.set_difficulty("easy"))
        easy_button.pack()
        medium_button = Button(self.window, text="Medium", font=("Bauhaus 93", 13), fg="#FFFFFF", bg="#FE8B32", image=self.difficulty_image, compound="center", command=lambda: self.set_difficulty("medium"))
        medium_button.pack()
        hard_button = Button(self.window, text="Hard", font=("Bauhaus 93", 13), fg="#FFFFFF", bg="#FE283C", image=self.difficulty_image, compound="center", command=lambda: self.set_difficulty("hard"))
        hard_button.pack()

        # Bind the animate_button function to the mouseover event of the difficulty buttons
        easy_button.bind("<Enter>", lambda event: animate_button(easy_button))
        medium_button.bind("<Enter>", lambda event: animate_button(medium_button))
        hard_button.bind("<Enter>", lambda event: animate_button(hard_button))

    def submit_name(self):
        # Get the name from the entry field
        name = self.name_entry.get().strip()
        if not name:
            # Display a warning message if name is empty
            messagebox.showwarning("Incomplete Information", "Please enter your name first.")
            return

        # Store the name and display the name label
        self.fullname = name
        if self.name_label is None:
            self.name_label = Label(self.window, text=f"Welcome\n {self.fullname}!", font=("Arial", 14), fg="#FFFFFF", bg="#1F4C93")
            self.name_label.place(x=65, y=150)
        else:
            self.name_label.config(text=f"Welcome\n {self.fullname}!")

        # Clear the name entry field and disable it
        self.name_entry.delete(0, END)
        self.name_entry.config(state=DISABLED)

    def set_difficulty(self, diff):
        # Check if a name has been entered before setting the difficulty
        if self.fullname is None:
            messagebox.showwarning("Incomplete Information", "Please enter your name first.")
            return

        # Set the difficulty and start the quiz
        self.difficulty = diff
        self.start_quiz()

    def start_quiz(self):
        # Destroy the window and start the quiz
        self.window.destroy()
        question_bank = get_data(self.difficulty)
        quiz = QuizBrain(question_bank)
        quiz_ui = QuizInterface(quiz, difficulty=self.difficulty)

    def run(self):
        # Run the main event loop
        self.window.mainloop()


if __name__ == '__main__':
    # Create an instance of the TrivialGame class and run the game
    game = TrivialGame()
    game.run()

