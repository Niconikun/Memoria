import tkinter as tk
from PIL import Image, ImageTk  # For image display

def show_next_content():
    global current_page
    current_page += 1

    # Clear any existing content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Display content for the current page
    if current_page == 1:
        label = tk.Label(content_frame, text="This is the first page!")
        label.pack()
    elif current_page == 2:
        label = tk.Label(content_frame, text="This is the second page!")
        label.pack()

        image = Image.open("cee-revista.jpg")  # Replace with your image path
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(window, image=photo)
        image_label.pack()

        label = tk.Label(text="Bienvenido de Nuevo")
        label.pack()

        text_input = tk.Entry(window)
        text_input.pack()

        next_button.config(text="Finish")  # Change button text on the last page
    else:
        window.destroy()  # Close the window after the last page

# Create the main window
window = tk.Tk()
window.title("Reliability DSM Simulator")

# Create a frame to hold the changing content
content_frame = tk.Frame(window)
content_frame.pack()

# Create the "Next" button
next_button = tk.Button(window, text="Next", command=show_next_content)
next_button.pack()

# Start with the first page
current_page = 0
show_next_content()  # Display the initial content

# Start the GUI event loop
window.mainloop()