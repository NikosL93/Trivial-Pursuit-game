import tkinter as tk
import time


class QuizTimer:  # Κλάση για τη δημιουργία του timer του κάθε γύρου ερωτήσεων
    def __init__(self, root, submit_answers):
        self.root = root
        self.submit_answers = submit_answers  # Παράμετρος που ενεργοποιεί την gameover στο quiz_ui
        self.font_style = ("Consolas", 14)
        self.total_time = 180  # Ο χρόνος σε sec για τον κάθε γύρο
        self.remaining_time = self.total_time  # Αρχικοποίηση του εναπομείναντα χρόνου του γύρου
        self.question_timer = Timer()  # Αρχικοποίηση της μεταβλητής μέσω της class Timer (αφορά το timer κάθε ερώτησης)
        self.question_timer.start()  # Έναρξη του timer της κάθε ερώτησης (μέσω της μεθόδου start())
        # Κατασκευή του label για εμφάνιση των χρόνων στην οθόνη
        self.timer_label = tk.Label(self.root, text="Time remaining: {} sec".format(self.total_time),
                                    font=self.font_style, bg="black", foreground="white")
        self.timer_label.pack(fill=tk.BOTH, padx=50, pady=2, side=tk.TOP, expand=True)
        self.start_time = time.time()  # Έναρξη του timer του γύρου ερωτήσεων
        self.run = None  # Αρχικοποίηση της μεταβλητής self.run σε None για τους ελέγχους
        self.run_timer()  # Έναρξη του timer του κάθε γύρου μέσω της μεθόδου run_timer()

    def run_timer(self):  # Συνάρτηση η οποία ανανεώνει τους μετρητές χρόνου του γύρου και της κάθε ερώτησης
        elapsed_time = int(time.time() - self.start_time)  # Υπολογισμός του χρόνου που περνάει (μέσω time module)
        self.remaining_time = self.total_time - elapsed_time  # Υπολογισμός του χρόνου που απομένει
        if self.remaining_time <= 0:  # Έλεγχος του εναπομείναντα χρόνου
            self.timer_label.config(text="Time is up!")
            self.submit_answers()  # Ενεργοποίηση της παραμέτρου(μεθόδου) η οποία τερματίζει τον γύρο όταν τελειώσει ο χρόνος
        else:
            # Σε ένα label εμφανίζεται ο χρόνος του γύρου και ο χρόνος που τρέχει για κάθε ερώτηση μέχρι να απαντηθεί
            question_elapsed_time = round(self.question_timer.elapsed_time())  # Στρογγυλοποίηση της τιμής του χρόνου της κάθε ερώτησης
            self.timer_label.config(
                text="Quiz Time remaining: {} sec\nQuestion Timer: {} sec".format(self.remaining_time,
                                                                                  question_elapsed_time))
            self.run = self.root.after(100, self.run_timer)

    def restart_timer(self):  # Μέθοδος για την επανέναρξη του timer όλου του γύρου ερωτήσεων
        if self.run is not None:
            self.root.after_cancel(self.run)  # Ακύρωση της self.run μέσω της after_cancel()
            self.run = None
        self.total_time = 180
        self.remaining_time = self.total_time
        self.start_time = time.time()
        self.run_timer()

    def stop_timer(self):  # Μέθοδος για τη διακοπή του timer του γύρου
        if self.run is not None:
            self.root.after_cancel(self.run)  # Ακύρωση της self.run μέσω της after_cancel()
            self.run = None

    def get_remaining_time(self):  # Μέθοδος που επιστρέφει τον εναπομείναντα χρόνο του γύρου
        return self.remaining_time

    def reset_question_timer(self):  # Μέθοδος επανεκκίνησης του timer της κάθε ερώτησης
        self.question_timer.start()


class Timer:  # Κλάση για τις λειτουργίες του timer των ερωτήσεων
    def __init__(self):
        self.start_time = None

    def start(self):  # Έναρξη του timer της κάθε ερώτησης
        self.start_time = time.perf_counter()

    def stop(self):  # Διακοπή του timer της κάθε ερώτησης. Η μέθοδος επίσης επιστρέφει τον χρόνο που πέρασε απο τη start()
        if self.start_time is None:
            print("Timer has not started yet. Call start() before calling stop().")
            return 0
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None  # Reset the timer
        return elapsed_time

    def elapsed_time(self):  # Μέθοδος που επιστρέφει τον χρόνο που πέρασε απο τη start()
        if self.start_time is None:
            return 0
        else:
            return time.perf_counter() - self.start_time
