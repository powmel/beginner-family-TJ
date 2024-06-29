import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

class MoodRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Recorder")

        self.label_date = tk.Label(root, text="記録する日付を選択してください:")
        self.label_date.grid(row=0, column=0, pady=5, padx=5)

        self.calendar = Calendar(root, selectmode='day')
        self.calendar.grid(row=1, column=0, pady=5, padx=5)

        self.label_time = tk.Label(root, text="記録する時刻を選択してください:")
        self.label_time.grid(row=0, column=1, pady=5, padx=5)

        self.time_frame = tk.Frame(root)
        self.time_frame.grid(row=1, column=1, pady=5, padx=5)

        self.hours = [f"{h:02d}" for h in range(24)]
        self.minutes = [f"{m:02d}" for m in range(60)]

        self.hour_combobox = ttk.Combobox(self.time_frame, values=self.hours, width=3, state="readonly")
        self.hour_combobox.set(datetime.now().strftime("%H"))
        self.hour_combobox.pack(side=tk.LEFT, padx=5)

        self.minute_combobox = ttk.Combobox(self.time_frame, values=self.minutes, width=3, state="readonly")
        self.minute_combobox.set(datetime.now().strftime("%M"))
        self.minute_combobox.pack(side=tk.LEFT, padx=5)

        self.label_health = tk.Label(root, text="体調はどうですか？")
        self.label_health.grid(row=2, column=0, pady=5, padx=5)
        
        self.health_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, label="1 (最悪) 〜 5 (最高)")
        self.health_scale.grid(row=3, column=0, pady=5, padx=5)
        
        self.label_mood = tk.Label(root, text="気分はどうですか？")
        self.label_mood.grid(row=2, column=1, pady=5, padx=5)
        
        self.mood_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, label="1 (最悪) 〜 5 (最高)")
        self.mood_scale.grid(row=3, column=1, pady=5, padx=5)

        self.label_memo = tk.Label(root, text="メモ（どんな状況だったか、何時に気分が悪かったかなど）")
        self.label_memo.grid(row=4, column=0, columnspan=2, pady=10, padx=5)

        self.textbox_memo = tk.Text(root, height=10, width=50)
        self.textbox_memo.grid(row=5, column=0, columnspan=2, pady=10, padx=5)

        self.save_button = tk.Button(root, text="保存", command=self.save_mood)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10, padx=5)

    def save_mood(self):
        date = self.calendar.get_date()
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()
        timestamp = f"{date} {hour}:{minute}"

        health = self.health_scale.get()
        mood = self.mood_scale.get()
        memo = self.textbox_memo.get("1.0", tk.END).strip()
        
        if memo:
            with open("mood_log.txt", "a") as file:
                file.write(f"{timestamp}\n体調: {health}/5\n気分: {mood}/5\nメモ: {memo}\n\n")
            messagebox.showinfo("保存完了", "気分が記録されました。")
            self.textbox_memo.delete("1.0", tk.END)
            self.health_scale.set(1)
            self.mood_scale.set(1)
        else:
            messagebox.showwarning("警告", "メモを入力してください。")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodRecorderApp(root)
    root.mainloop()
