import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import subprocess  # Added to call mainscene.py and mood_viewer.py

class MoodRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Recorder")
        self.root.configure(bg="#FFF4E0")  # 背景色を設定

        self.label_date = tk.Label(root, text="記録する日付を選択してください:", fg="#543E27", bg="#FFF4E0")
        self.label_date.grid(row=0, column=0, pady=5, padx=5)

        self.calendar = Calendar(root, selectmode='day')
        self.calendar.grid(row=1, column=0, pady=5, padx=5)

        self.label_time = tk.Label(root, text="記録する時刻を選択してください:", fg="#543E27", bg="#FFF4E0")
        self.label_time.grid(row=0, column=1, pady=5, padx=5)

        self.time_frame = tk.Frame(root,bg="#FFF4E0")
        self.time_frame.grid(row=1, column=1, pady=5, padx=5)

        self.hours = [f"{h:02d}" for h in range(24)]
        self.minutes = [f"{m:02d}" for m in range(60)]

        self.hour_combobox = ttk.Combobox(self.time_frame, values=self.hours, width=3, state="readonly")
        self.hour_combobox.set(datetime.now().strftime("%H"))
        self.hour_combobox.pack(side=tk.LEFT, padx=5)

        self.minute_combobox = ttk.Combobox(self.time_frame, values=self.minutes, width=3, state="readonly")
        self.minute_combobox.set(datetime.now().strftime("%M"))
        self.minute_combobox.pack(side=tk.LEFT, padx=5)

        self.label_health = tk.Label(root, text="体調はどうですか？",fg="#543E27", bg="#FFF4E0")
        self.label_health.grid(row=2, column=0, pady=5, padx=5)
        
        self.health_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, label="1 (最悪) 〜 5 (最高)", fg="#543E27", bg="#FFF4E0")
        self.health_scale.grid(row=3, column=0, pady=5, padx=5)
        
        self.label_mood = tk.Label(root, text="気分はどうですか？",fg="#543E27", bg="#FFF4E0")
        self.label_mood.grid(row=2, column=1, pady=5, padx=5)
        
        self.mood_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, label="1 (最悪) 〜 5 (最高)", fg="#543E27", bg="#FFF4E0")
        self.mood_scale.grid(row=3, column=1, pady=5, padx=5)

        self.label_memo = tk.Label(root, text="メモ（どんな状況だったか、何時に気分が悪かったかなど）", fg="#543E27", bg="#FFF4E0")
        self.label_memo.grid(row=4, column=0, columnspan=2, pady=5, padx=5)
        
        self.textbox_memo = tk.Text(root, height=5, width=40)
        self.textbox_memo.grid(row=5, column=0, columnspan=2, pady=5, padx=5)

        self.save_button = tk.Button(root, text="記録を保存", command=self.save_record)
        self.save_button.grid(row=6, column=0, pady=5, padx=5)

        self.view_button = tk.Button(root, text="記録を見る", command=self.view_record)
        self.view_button.grid(row=6, column=1, pady=5, padx=5)

        # Adding the "Return to Main Screen" button
        self.return_button = tk.Button(root, text="メイン画面に戻る", command=self.return_to_main)
        self.return_button.grid(row=7, column=0, columnspan=2, pady=5, padx=5)


    def save_record(self):
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

    def view_record(self):
        # Placeholder for view logic
        messagebox.showinfo("表示", "記録を表示します！")
        self.root.destroy()
        subprocess.Popen(["python", "mood_viewer.py"])  # Call mood_viewer.py

    def return_to_main(self):
        self.root.destroy()
        subprocess.Popen(["python", "mainscene.py"])  # Call mainscene.py

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodRecorderApp(root)
    root.mainloop()