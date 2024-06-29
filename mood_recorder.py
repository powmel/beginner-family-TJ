import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class MoodRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Recorder")

        self.label_date = tk.Label(root, text="Select the date:")
        self.label_date.pack(pady=5)

        self.date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        self.label_time = tk.Label(root, text="Select the time:")
        self.label_time.pack(pady=5)

        self.hours = [f"{h:02d}" for h in range(24)]
        self.minutes = [f"{m:02d}" for m in range(60)]

        self.hour_combobox = ttk.Combobox(root, values=self.hours, width=3, state="readonly")
        self.hour_combobox.set(datetime.now().strftime("%H"))
        self.hour_combobox.pack(side=tk.LEFT, padx=5)

        self.minute_combobox = ttk.Combobox(root, values=self.minutes, width=3, state="readonly")
        self.minute_combobox.set(datetime.now().strftime("%M"))
        self.minute_combobox.pack(side=tk.LEFT, padx=5)

        self.label_health = tk.Label(root, text="How is your health?")
        self.label_health.pack(pady=5)
        
        self.health_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, label="1 (Worst) to 5 (Best)")
        self.health_scale.pack(pady=5)
        
        self.label_mood = tk.Label(root, text="How is your mood?")
        self.label_mood.pack(pady=5)
        
        self.mood_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, label="1 (Worst) to 5 (Best)")
        self.mood_scale.pack(pady=5)

        self.label_memo = tk.Label(root, text="Memo (what happened, time of bad mood, etc.)")
        self.label_memo.pack(pady=10)

        self.textbox_memo = tk.Text(root, height=10, width=50)
        self.textbox_memo.pack(pady=10)

        self.save_button = tk.Button(root, text="Save", command=self.save_mood)
        self.save_button.pack(pady=10)

    def save_mood(self):
        date = self.date_entry.get()
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()
        timestamp = f"{date} {hour}:{minute}"

        health = self.health_scale.get()
        mood = self.mood_scale.get()
        memo = self.textbox_memo.get("1.0", tk.END).strip()
        
        if memo:
            with open("mood_log.txt", "a") as file:
                file.write(f"{timestamp}\nHealth: {health}/5\nMood: {mood}/5\nMemo: {memo}\n\n")
            messagebox.showinfo("Saved", "Your mood has been recorded.")
            self.textbox_memo.delete("1.0", tk.END)
            self.health_scale.set(1)
            self.mood_scale.set(1)
        else:
            messagebox.showwarning("Warning", "Please enter a memo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodRecorderApp(root)
    root.mainloop()
