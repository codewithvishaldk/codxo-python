import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import random

class NumberGuessingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game")
        self.geometry("400x300")
        self.style = Style(theme='cosmo')
        self.attempts = 0
        self.number_to_guess = random.randint(1, 100)
        
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Guess the Number", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        self.instruction_label = ttk.Label(self, text="I'm thinking of a number between 1 and 100.", font=("Helvetica", 12))
        self.instruction_label.pack(pady=10)

        self.entry = ttk.Entry(self, font=("Helvetica", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        self.guess_button = ttk.Button(self, text="Guess", command=self.check_guess)
        self.guess_button.pack(pady=10)

        self.result_label = ttk.Label(self, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1

            if guess < self.number_to_guess:
                self.result_label.config(text="Too low!", foreground="red")
            elif guess > self.number_to_guess:
                self.result_label.config(text="Too high!", foreground="red")
            else:
                self.result_label.config(text=f"Congratulations! You guessed the number {self.number_to_guess} in {self.attempts} attempts.", foreground="green")
                self.show_confetti()
                self.guess_button.config(state="disabled")
                self.entry.config(state="disabled")

            self.animate_feedback()
        except ValueError:
            self.result_label.config(text="Please enter a valid number.", foreground="red")

    def animate_feedback(self):
        self.result_label.pack_forget()
        self.result_label.pack(pady=10)

    def show_confetti(self):
        canvas = tk.Canvas(self, width=400, height=300)
        canvas.pack()
        
        colors = ["red", "green", "blue", "yellow", "orange", "purple"]
        
        for _ in range(100):
            x = random.randint(0, 400)
            y = random.randint(0, 300)
            size = random.randint(5, 20)
            color = random.choice(colors)
            canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        
        canvas.after(3000, canvas.destroy)  # Destroy the canvas after 3 seconds

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.mainloop()
