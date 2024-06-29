import tkinter

def transition_button(widget):
    # ここにボタンを押した時の処理を書く。                                      
    print("clicked")

# ウィンドウの作成                                                              
window = tkinter.Tk()
window.geometry("400x400")
window.title("Screen Transition")

# 遷移前の画面の作成                                                            
canvas1 = tkinter.Canvas(background="#cea", width=400, height=400)
canvas1.place(x=0, y=0) # キャンバス                                            
label1 = tkinter.Label(canvas1, text="遷移する前の画面です。") # テキスト       
label1.place(x=200, y=150, anchor=tkinter.CENTER)
button = tkinter.Button(canvas1, text="遷移するボタン", command=lambda:transition_button(canvas1)) # 遷移ボタン                                                
button.place(x=200, y=250, anchor=tkinter.CENTER)

window.mainloop()