import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import os

class MoodViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Viewer")

        self.label = tk.Label(root, text="日付を選択して記録を表示:")
        self.label.pack(pady=10)

        self.calendar = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(pady=10)

        self.show_button = tk.Button(root, text="表示", command=self.show_mood)
        self.show_button.pack(pady=10)

        self.textbox = tk.Text(root, height=10, width=50)
        self.textbox.pack(pady=10)

        self.load_records()

    def load_records(self):
        self.records = {}
        if os.path.exists("mood_log.txt"):
            with open("mood_log.txt", "r") as file:
                lines = file.readlines()
                current_record = []
                current_date = None
                for line in lines:
                    if line.strip() == "":
                        if current_record:
                            self.records[current_date] = current_record
                        current_record = []
                    elif line.startswith("20"):  # assuming date lines start with '20'
                        current_date = line.split()[0]
                        current_record = [line.strip()]
                    else:
                        current_record.append(line.strip())

    def show_mood(self):
        selected_date = self.calendar.get_date()
        self.textbox.delete("1.0", tk.END)
        if selected_date in self.records:
            for entry in self.records[selected_date]:
                self.textbox.insert(tk.END, entry + "\n")
        else:
            self.textbox.insert(tk.END, "記録がありません。")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodViewerApp(root)
    root.mainloop()
