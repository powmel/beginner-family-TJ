import tkinter as tk
from tkinter import ttk

# メインウィンドウの作成
root = tk.Tk()
root.title("セッションを選ぼう")

# セッションフレームの作成
def create_session_frame(parent, color):
    frame = tk.Frame(parent, bg=color, padx=10, pady=10)
    frame.pack(fill='both', expand=True, padx=10, pady=5)
    button = ttk.Button(frame, text="参加する")
    button.pack(side='right')
    return frame

# タイトルラベルの作成
title_label = tk.Label(root, text="セッションを選ぼう", font=("Arial", 14))
title_label.pack(pady=10)

# セッションフレームの作成と配置
frame1 = create_session_frame(root, 'lightblue')
frame2 = create_session_frame(root, 'skyblue')
frame3 = create_session_frame(root, 'lightcoral')

# メインループの開始
root.mainloop()