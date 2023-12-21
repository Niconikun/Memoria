import tkinter as tk
from PIL import Image, ImageTk  # For image display

# Create the main window
root = tk.Tk()
root.title("Reliability DSM Simulator")

label = tk.Label(text="Bienvenido de Nuevo")
label.pack()

# Create a text input field
text_input = tk.Entry(root)
text_input.pack()

# Create a button
button = tk.Button(root, text="Click Me!")
button.pack()

# Load and display an image
image = Image.open("cee-revista.jpg")  # Replace with your image path
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.pack()

# Start the GUI event loop
root.mainloop()