import tkinter as tk

def create_main_window():
    window = tk.Tk()
    window.title("通話アプリ")
    
    # モード変更ボタン
    mode_button = tk.Button(window, text="モード変更")
    mode_button.pack()

    # ソートボタン
    sort_button = tk.Button(window, text="ソート")
    sort_button.pack()

    # リスト表示エリア
    list_frame = tk.Frame(window)
    list_frame.pack()

    for i in range(5):  # ダミーのリスト項目
        item = tk.Label(list_frame, text=f"項目 {i+1}")
        item.pack()

    # 参加ボタン
    join_button = tk.Button(window, text="参加")
    join_button.pack()

    # 通話画面ボタン
    call_frame = tk.Frame(window)
    call_frame.pack()
    for i in range(6):
        button = tk.Button(call_frame, text=f"参加者 {i+1}")
        button.grid(row=i//3, column=i%3)

    # 日記などのボタン
    diary_button = tk.Button(window, text="日記")
    diary_button.pack()

    window.mainloop()

create_main_window()
