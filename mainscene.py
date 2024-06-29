import tkinter as tk
import subprocess

# メインアプリケーションクラス
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("メイン画面")
        self.geometry("300x200")

        # 「セッションを選ぶ」ボタン
        self.session_button = tk.Button(self, text="セッションを選ぶ", command=self.show_session_page, width=20, height=3)
        self.session_button.pack(pady=20)

        # 「日記を書く・読む」ボタン
        self.diary_button = tk.Button(self, text="日記を書く・読む", command=self.show_diary_page, width=20, height=3)
        self.diary_button.pack(pady=20)

    # 「セッションを選ぶ」ページを表示するメソッド
    def show_session_page(self):
        self.destroy()  # メイン画面を削除
        subprocess.Popen(["python", "sessionSelecter.py"])  # sessionSelecter.py を実行

    # 「日記を書く・読む」ページを表示するメソッド
    def show_diary_page(self):
        self.clear_screen()
        DiaryPage(self)

    # 画面をクリアするメソッド
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # メインメニューを再表示するメソッド
    def show_main_menu(self):
        self.clear_screen()
        self.session_button.pack(pady=20)
        self.diary_button.pack(pady=20)

# 「日記を書く・読む」ページクラス
class DiaryPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack()

        self.label = tk.Label(self, text="日記を書く・読むページ")
        self.label.pack(pady=20)

        self.back_button = tk.Button(self, text="戻る", command=self.go_back)
        self.back_button.pack(pady=20)

    def go_back(self):
        self.pack_forget()
        self.parent.show_main_menu()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
