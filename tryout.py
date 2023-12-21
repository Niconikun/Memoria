import tkinter as tk

def say_hello():
    name = input_field.get()
    message = f"Hello, {name}!"
    greeting.config(text=message)

window = tk.Tk()

label = tk.Label(window, text="Enter your name:")
label.pack()
input_field = tk.Entry(window)
input_field.pack()

button = tk.Button(window, text="Say Hello", command=say_hello)
button.pack()

greeting = tk.Label(window, text="")
greeting.pack()

window.mainloop()
