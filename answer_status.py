import tkinter as tk


class AnswerInfoLabel:  # Κλάση που δημιουργεί το label (στο frame των ερωτήσεων)

    def __init__(self, root):
        self.label_text = tk.StringVar()
        self.label = tk.Label(root, textvariable=self.label_text, font=("Consolas", 11), background="#747780")
        self.label.pack(anchor="n", pady=(0, 5))

    def update_label(self, new_text):
        self.label_text.set(new_text)
