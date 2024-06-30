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
        self.label_memo.grid(row=4, column=0, columnspan=2, pady=5, padx=5)
        
        self.memo_text = tk.Text(root, height=5, width=40)
        self.memo_text.grid(row=5, column=0, columnspan=2, pady=5, padx=5)

        self.save_button = tk.Button(root, text="記録を保存", command=self.save_record)
        self.save_button.grid(row=6, column=0, pady=5, padx=5)

        self.view_button = tk.Button(root, text="記録を見る", command=self.view_record)
        self.view_button.grid(row=6, column=1, pady=5, padx=5)

        # Adding the "Return to Main Screen" button
        self.return_button = tk.Button(root, text="メイン画面に戻る", command=self.return_to_main)
        self.return_button.grid(row=7, column=0, columnspan=2, pady=5, padx=5)

    def save_record(self):
        # Placeholder for save logic
        messagebox.showinfo("保存", "記録が保存されました！")

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
