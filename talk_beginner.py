import tkinter as tk
from tkinter import messagebox

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")

        # メインウィンドウ
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # トークのリスト
        self.talks = ["Talk 1", "Talk 2", "Talk 3"]

        self.talk_listbox = tk.Listbox(self.main_frame)
        for talk in self.talks:
            self.talk_listbox.insert(tk.END, talk)
        self.talk_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.select_button = tk.Button(self.main_frame, text="Select Talk", command=self.open_talk)
        self.select_button.pack(pady=10)

    def open_talk(self):
        selected_index = self.talk_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a talk.")
            return

        selected_talk = self.talk_listbox.get(selected_index)

        # トーク画面の作成
        self.talk_window = tk.Toplevel(self.root)
        self.talk_window.title(selected_talk)

        self.chat_frame = tk.Frame(self.talk_window)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_text = tk.Text(self.chat_frame, state=tk.DISABLED)
        self.chat_text.pack(fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self.talk_window)
        self.entry_frame.pack(fill=tk.X, padx=10, pady=10)

        self.message_entry = tk.Entry(self.entry_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def send_message(self):
        message = self.message_entry.get()
        if message.strip():
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.insert(tk.END, f"You: {message}\n")
            self.chat_text.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
