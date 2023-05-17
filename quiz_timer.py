import tkinter as tk
import time

class QuizTimer:
    def __init__(self, root, submit_answers):
        self.root = root
        self.submit_answers = submit_answers
        self.font_style = ("Consolas", 14)
        self.total_time = 180
        self.remaining_time = self.total_time
        self.timer_label = tk.Label(self.root, text="Time remaining: {} sec".format(self.total_time), font=self.font_style, bg="#747780", background="black", foreground="white")
        self.timer_label.pack(fill=tk.BOTH, padx=50, pady=2, side=tk.TOP, expand=True)
        self.start_time = time.time()
        self.run = None
        self.run_timer()

    def run_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.remaining_time = self.total_time - elapsed_time
        if self.remaining_time <= 0:
            self.timer_label.config(text="Time is up!")
            self.submit_answers()
        else:
            self.timer_label.config(text="Time remaining: {} sec".format(self.remaining_time))
            self.run = self.root.after(50, self.run_timer)

    def restart_timer(self):
        if self.run is not None:
            self.root.after_cancel(self.run)  # Ακύρωση της self.run μέσω της after_cancel()
            self.run = None
        self.total_time = 30
        self.remaining_time = self.total_time
        self.start_time = time.time()
        self.run_timer()

    def stop_timer(self):
        if self.run is not None:
            self.root.after_cancel(self.run)  # Ακύρωση της self.run μέσω της after_cancel()
            self.run = None

    def get_remaining_time(self):
        return self.remaining_time



