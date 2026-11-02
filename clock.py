import tkinter as tk
from time import strftime

clock = tk.Label(tk.Tk(), font=("Arial", 48), padx=20, pady=10)
window = clock.master
clock.pack()

def update_clock():
	clock.config(text=strftime("%H:%M:%S"))
	window.after(1000, update_clock)

update_clock()
window.mainloop()
