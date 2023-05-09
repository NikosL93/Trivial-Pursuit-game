import tkinter as tk
import time

class QuizTimer:
    def __init__(self, root, submit_answers):
        self.root = root
        self.submit_answers = submit_answers
        self.font_style = ("Consolas", 14)
        self.total_time = 180
        self.timer_label = tk.Label(self.root, text="Time remaining: {} sec".format(self.total_time), font=self.font_style, bg="#747780")
        self.timer_label.pack(fill=tk.BOTH, padx=10, pady=7, side=tk.TOP, expand=True)
        self.start_time = time.time()
        self.run_timer()

    def run_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.total_time - elapsed_time
        if remaining_time <= 0:
            self.timer_label.config(text="Time is up!")
            self.submit_answers()
        else:
            self.timer_label.config(text="Time remaining: {} sec".format(remaining_time))
            self.root.after(50, self.run_timer)
