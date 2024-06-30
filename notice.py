import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import win32com.client

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diary App")

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.write_diary_button = tk.Button(self.button_frame, text="日記を書く", command=self.show_write_diary_page)
        self.write_diary_button.pack(side=tk.RIGHT, padx=10)

    def show_write_diary_page(self):
        self.diary_window = tk.Toplevel(self.root)
        self.diary_window.title("Write Diary")

        tk.Label(self.diary_window, text="Date/Time:").pack()
        self.datetime_entry = tk.Entry(self.diary_window)
        self.datetime_entry.pack()

        tk.Label(self.diary_window, text="Health (1-5):").pack()
        self.health_entry = tk.Entry(self.diary_window)
        self.health_entry.pack()

        tk.Label(self.diary_window, text="Mood (1-5):").pack()
        self.mood_entry = tk.Entry(self.diary_window)
        self.mood_entry.pack()

        tk.Label(self.diary_window, text="Memo:").pack()
        self.memo_entry = tk.Entry(self.diary_window)
        self.memo_entry.pack()

        submit_button = tk.Button(self.diary_window, text="Submit", command=self.submit_diary)
        submit_button.pack(pady=10)

    def submit_diary(self):
        datetime_str = self.datetime_entry.get()
        health = int(self.health_entry.get())
        mood = int(self.mood_entry.get())
        memo = self.memo_entry.get()

        diary_entry = f"{datetime_str}\nhealth: {health}/5\nmood: {mood}/5\nmemo: {memo}"
        print(diary_entry)

        # Check if notification needs to be scheduled
        if health == 1 or mood == 1:
            datetime_obj = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M')
            notification_time = datetime_obj + timedelta(days=1)
            self.schedule_notification(notification_time)

        self.diary_window.destroy()

    def schedule_notification(self, notification_time):
        # Windowsタスクスケジューラにタスクを追加
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        rootFolder = scheduler.GetFolder('\\')

        taskDef = scheduler.NewTask(0)

        # Create trigger
        trigger = taskDef.Triggers.Create(1)  # 1 = OneTimeTrigger
        trigger.StartBoundary = notification_time.isoformat()

        # Create action
        action = taskDef.Actions.Create(0)  # 0 = Execute
        action.Path = 'python'
        action.Arguments = 'C:\\path\\to\\notice.py'

        # Set parameters
        taskDef.RegistrationInfo.Description = 'Health or Mood Notification'
        taskDef.Settings.Enabled = True
        taskDef.Settings.StopIfGoingOnBatteries = False

        rootFolder.RegisterTaskDefinition(
            'HealthMoodNotification',
            taskDef,
            6,  # 6 = TASK_CREATE_OR_UPDATE
            None,
            None,
            3,  # 3 = TASK_LOGON_INTERACTIVE_TOKEN
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
