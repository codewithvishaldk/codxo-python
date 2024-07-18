import tkinter as tk
from tkinter import ttk
import random
import string
import math

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.geometry("500x350")

        # Initialize widgets
        self.create_widgets()

    def create_widgets(self):
        # Length label and entry
        self.length_label = ttk.Label(self, text="Password Length:")
        self.length_label.grid(row=0, column=0, padx=10, pady=10)

        self.length_entry = ttk.Entry(self, width=15, font=('Helvetica', 12))
        self.length_entry.grid(row=0, column=1, padx=10, pady=10)
        self.length_entry.insert(0, "12")  # Default length

        # Options for including characters
        self.include_letters = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_specials = tk.BooleanVar(value=True)

        self.letters_checkbox = ttk.Checkbutton(self, text="Include Letters", variable=self.include_letters)
        self.letters_checkbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.digits_checkbox = ttk.Checkbutton(self, text="Include Digits", variable=self.include_digits)
        self.digits_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.specials_checkbox = ttk.Checkbutton(self, text="Include Special Characters", variable=self.include_specials)
        self.specials_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Generate button
        self.generate_button = ttk.Button(self, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Copy button
        self.copy_button = ttk.Button(self, text="Copy Password", command=self.copy_password, state=tk.DISABLED)
        self.copy_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Result label
        self.result_label = ttk.Label(self, text="", font=('Helvetica', 14, 'bold'))
        self.result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Strength and time label
        self.strength_label = ttk.Label(self, text="", font=('Helvetica', 12))
        self.strength_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length <= 0:
                self.result_label.config(text="Length must be greater than 0.")
                return

            characters = ""
            if self.include_letters.get():
                characters += string.ascii_letters
            if self.include_digits.get():
                characters += string.digits
            if self.include_specials.get():
                characters += string.punctuation

            if not characters:
                self.result_label.config(text="At least one character type must be selected.")
                return

            password = ''.join(random.choice(characters) for _ in range(length))
            self.result_label.config(text=password)
            self.copy_button.config(state=tk.NORMAL)
            
            strength, time_to_crack = self.evaluate_password(password)
            self.strength_label.config(text=f"Strength: {strength}\nTime to Hack: {time_to_crack}")

        except ValueError:
            self.result_label.config(text="Please enter a valid number for length.")

    def copy_password(self):
        self.clipboard_clear()
        self.clipboard_append(self.result_label.cget("text"))
        self.update()  # Keep the clipboard content updated
        self.result_label.config(text="Password copied to clipboard!")

    def evaluate_password(self, password):
        length = len(password)
        unique_chars = len(set(password))
        entropy = unique_chars * math.log2(unique_chars) * length
        
        # Determine password strength
        if length < 8:
            strength = "Weak"
        elif 8 <= length < 12:
            strength = "Moderate"
        elif 12 <= length < 16:
            strength = "Strong"
        else:
            strength = "Very Strong"

        # Time to crack estimation
        attack_rate = 1e9  # guesses per second
        time_to_crack_seconds = math.pow(2, entropy) / attack_rate
        
        # Format time to crack into a readable format
        if time_to_crack_seconds < 60:
            time_str = f"{time_to_crack_seconds:.2f} seconds"
        elif time_to_crack_seconds < 3600:
            time_str = f"{time_to_crack_seconds / 60:.2f} minutes"
        elif time_to_crack_seconds < 86400:
            time_str = f"{time_to_crack_seconds / 3600:.2f} hours"
        elif time_to_crack_seconds < 31536000:
            time_str = f"{time_to_crack_seconds / 86400:.2f} days"
        elif time_to_crack_seconds < 3.154e+10:
            time_str = f"{time_to_crack_seconds / 31536000:.2f} years"
        else:
            time_str = f"{time_to_crack_seconds / 3.154e+10:.2f} centuries"

        return strength, time_str

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
