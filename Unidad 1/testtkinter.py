import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("My Application")
root.geometry("640x480")
root.minsize(400, 500)

ttk.Label(root, text="Hello").pack(padx=20, pady=20)

root.mainloop()