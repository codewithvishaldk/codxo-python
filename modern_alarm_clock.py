import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import time
import threading
import pygame

class AlarmClockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enhanced Alarm Clock")
        self.geometry("400x300")
        self.configure(bg="#2E2E2E")  # Dark background color

        # Initialize pygame mixer
        pygame.mixer.init()
        self.current_sound = pygame.mixer.Sound("rt-k931ixljmtqz7i-63188.mp3")  # Default sound
        self.alarm_channel = pygame.mixer.Channel(0)  # Create a separate channel for the alarm sound

        # Setup for alarm
        self.alarm_time = None
        self.snooze_time = 5  # Snooze duration in minutes

        # Create a frame for the clock display
        self.clock_frame = tk.Frame(self, bg="#2E2E2E")
        self.clock_frame.pack(pady=20)

        # Current time display
        self.current_time_label = tk.Label(
            self.clock_frame,
            font=("Arial", 36),
            bg="#2E2E2E",
            fg="#FFFFFF",
            padx=10,
            pady=10
        )
        self.current_time_label.pack()

        # Set alarm label and entry
        self.alarm_time_label = tk.Label(
            self,
            text="Set Alarm Time (HH:MM:SS):",
            font=("Arial", 14),
            bg="#2E2E2E",
            fg="#FFFFFF"
        )
        self.alarm_time_label.pack(pady=5)

        self.alarm_time_entry = tk.Entry(
            self,
            font=("Arial", 18),
            width=20
        )
        self.alarm_time_entry.pack(pady=5)

        # Set alarm button
        self.set_alarm_button = tk.Button(
            self,
            text="Set Alarm",
            command=self.set_alarm,
            font=("Arial", 14),
            bg="#4CAF50",
            fg="#FFFFFF",
            activebackground="#45A049",
            relief=tk.RAISED
        )
        self.set_alarm_button.pack(pady=10)

        # Snooze button
        self.snooze_button = tk.Button(
            self,
            text="Snooze",
            command=self.snooze_alarm,
            font=("Arial", 14),
            bg="#FFC107",
            fg="#FFFFFF",
            activebackground="#FFB300",
            relief=tk.RAISED
        )
        self.snooze_button.pack(pady=10)
        self.snooze_button.config(state=tk.DISABLED)

        # Custom alarm sound button
        self.custom_sound_button = tk.Button(
            self,
            text="Change Alarm Sound",
            command=self.change_alarm_sound,
            font=("Arial", 14),
            bg="#2196F3",
            fg="#FFFFFF",
            activebackground="#1976D2",
            relief=tk.RAISED
        )
        self.custom_sound_button.pack(pady=10)

        # Dark/Light mode toggle
        self.dark_mode = True
        self.toggle_mode_button = tk.Button(
            self,
            text="Switch to Light Mode",
            command=self.toggle_mode,
            font=("Arial", 14),
            bg="#FF5722",
            fg="#FFFFFF",
            activebackground="#E64A19",
            relief=tk.RAISED
        )
        self.toggle_mode_button.pack(pady=10)

        # Start the current time updating loop
        self.update_time()

        # Start the alarm checking thread
        self.check_alarm_thread = threading.Thread(target=self.check_alarm)
        self.check_alarm_thread.daemon = True
        self.check_alarm_thread.start()

    def update_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=now)
        self.after(1000, self.update_time)  # Update every second

    def set_alarm(self):
        self.alarm_time = self.alarm_time_entry.get()
        try:
            datetime.strptime(self.alarm_time, "%H:%M:%S")
            messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time}")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid time in HH:MM:SS format.")
        self.snooze_button.config(state=tk.DISABLED)

    def snooze_alarm(self):
        if self.alarm_time:
            alarm_time_obj = datetime.strptime(self.alarm_time, "%H:%M:%S")
            snooze_time_obj = alarm_time_obj + timedelta(minutes=self.snooze_time)
            self.alarm_time = snooze_time_obj.strftime("%H:%M:%S")
            messagebox.showinfo("Alarm Snoozed", f"Alarm snoozed to {self.alarm_time}")

    def change_alarm_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.current_sound = pygame.mixer.Sound(file_path)
            messagebox.showinfo("Sound Changed", "Alarm sound updated successfully!")

    def toggle_mode(self):
        if self.dark_mode:
            self.configure(bg="#FFFFFF")
            self.clock_frame.configure(bg="#FFFFFF")
            self.current_time_label.config(bg="#FFFFFF", fg="#000000")
            self.alarm_time_label.config(bg="#FFFFFF", fg="#000000")
            self.alarm_time_entry.config(bg="#F0F0F0")
            self.set_alarm_button.config(bg="#8BC34A", activebackground="#7CB342")
            self.snooze_button.config(bg="#FFC107", activebackground="#FFB300")
            self.custom_sound_button.config(bg="#2196F3", activebackground="#1976D2")
            self.toggle_mode_button.config(text="Switch to Dark Mode", bg="#9E9E9E", activebackground="#757575")
        else:
            self.configure(bg="#2E2E2E")
            self.clock_frame.configure(bg="#2E2E2E")
            self.current_time_label.config(bg="#2E2E2E", fg="#FFFFFF")
            self.alarm_time_label.config(bg="#2E2E2E", fg="#FFFFFF")
            self.alarm_time_entry.config(bg="#424242")
            self.set_alarm_button.config(bg="#4CAF50", activebackground="#45A049")
            self.snooze_button.config(bg="#FFC107", activebackground="#FFB300")
            self.custom_sound_button.config(bg="#2196F3", activebackground="#1976D2")
            self.toggle_mode_button.config(text="Switch to Light Mode", bg="#FF5722", activebackground="#E64A19")
        self.dark_mode = not self.dark_mode

    def check_alarm(self):
        while True:
            if self.alarm_time:
                current_time = datetime.now().strftime("%H:%M:%S")
                if current_time == self.alarm_time:
                    self.alarm_time = None  # Clear the alarm
                    self.start_alarm()
                    self.snooze_button.config(state=tk.NORMAL)
            time.sleep(1)  # Check every second

    def start_alarm(self):
        # Play the alarm sound immediately
        self.alarm_channel.play(self.current_sound, loops=-1)
        # Show the alarm notification
        self.show_alarm_notification()

    def stop_alarm(self):
        # Stop the alarm sound
        self.alarm_channel.stop()

    def show_alarm_notification(self):
        def on_ok():
            self.stop_alarm()
            self.dialog.destroy()
        
        # Show the alarm notification with OK button
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Alarm")
        self.dialog.geometry("300x100")
        self.dialog.configure(bg="#2E2E2E")
        
        msg = tk.Label(
            self.dialog,
            text="Wake up! Your alarm is ringing!",
            font=("Arial", 14),
            bg="#2E2E2E",
            fg="#FFFFFF"
        )
        msg.pack(pady=10)
        
        ok_button = tk.Button(
            self.dialog,
            text="OK",
            command=on_ok,
            font=("Arial", 14),
            bg="#4CAF50",
            fg="#FFFFFF",
            activebackground="#45A049",
            relief=tk.RAISED
        )
        ok_button.pack(pady=5)

if __name__ == "__main__":
    app = AlarmClockApp()
    app.mainloop()
