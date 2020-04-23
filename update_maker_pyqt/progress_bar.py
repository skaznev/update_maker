from tkinter import *
import tkinter.ttk as ttk
import time, threading
root = Tk()

pb = ttk.Progressbar(root, mode="determinate" , )
pb.pack()
#pb['maximum'] = 50
def progress():
    for i in range(50):
        pb['value'] += i
        time.sleep(.3)

threading.Thread(target=progress).start()
root.mainloop()