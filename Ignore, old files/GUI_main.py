from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # For image display
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Reliability

'''
Ignore this file, it doesn't serve a functional purpose. The purpose of this code is to
implement a Graphic User Interface, implementing the similar instructions as
in Main_est. It has been discontinued to pursue other priorities.
'''

def destroy():
    window.destroy()

window = Tk()
window.title("Reliability DSM Simulator")
window.geometry('750x500')

# Create a frame to hold the changing content
tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)

tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='DSM Diagram')

tab_control.add(tab2, text='System Engineering Envelopes')

#label = Label(tab1, text="Welcome back!")
#label.pack()

lbl1_1 = Label(tab1, text= '¿Cuál es la cantidad de satélites mínimos que debe componer el cluster? Ingrese un número: ')

lbl1_1.grid(column=0, row=0)

spin_1 = Spinbox(tab1, from_=1, to=10, width=5)

spin_1.grid(column=1,row=0)

lbl1_2 = Label(tab1, text="¿Cuál es la cantidad de satélites a comenzar? Ingrese un número: ")

lbl1_2.grid(column=0, row= 1)

spin_2 = Spinbox(tab1, from_=1, to=10, width=5)

spin_2.grid(column=1,row=1)

lbl2_2 = Label(tab1, text="EPS posee redundancia? ")

lbl2_2.grid(column=0, row= 2)

EPS_red_yes = Radiobutton(tab1, text="Yes", variable=False, value=0)
EPS_red_yes.grid(column=0, row=3)
EPS_red_no = Radiobutton(tab1, text="No", variable=True, value=1)
EPS_red_no.grid(column=1, row=3)

lbl3 = Label(tab1, text= 'Parámetros de la Misión')

lbl3.grid(column=0, row=4)

lbl4 = Label(tab1, text= '¿Cuánto dura la misión? Ingrese un número:')

lbl4.grid(column=0, row=6)

spin_3 = Spinbox(tab1, from_=1, to=10, width=5)

spin_3.grid(column=1,row=6)

lbl5 = Label(tab1, text= 'Parámetros de Mitigación')

lbl5.grid(column=0, row=7)

lbl6 = Label(tab1, text= '¿Despliegue en Fase?')

lbl6.grid(column=0, row=9)

Fase_yes = Radiobutton(tab1, text="Yes", variable=False, value=2)
Fase_yes.grid(column=0, row=10)
Fase_no = Radiobutton(tab1, text="No", variable=True, value=3)
Fase_no.grid(column=1, row=10)

tab_control.pack(expand=1, fill='both')


window.mainloop()

# Create the "Next" button
#next_button = tk.Button(tab2, text="Next")
#next_button.pack()


#def show_next_content():
 #   global current_page
  #  current_page += 1

    # Clear any existing content
   # for widget in content_frame.winfo_children():
    #    widget.destroy()

    # Display content for the current page
    #if current_page == 1:
     #   image_dim = Image.open("DIM blue.png")  # Replace with your image path
      #  photo = ImageTk.PhotoImage(image_dim,size=0.5)
       # etiqueta = tk.Label(window, image=image_dim)
        #etiqueta.pack()


        #image = Image.open("cee-revista.jpg")  # Replace with your image path
        #photo = ImageTk.PhotoImage(image)
        #image_label = tk.Label(window, image=photo)
        #image_label.pack()

        #label = tk.Label(text="Bienvenido de Nuevo")
        #label.pack()

    #    text_input = tk.Entry(window)
   #     text_input.pack()

    #elif current_page == 4:
     #   label = tk.Label(content_frame, text="This is the Template page!")
   #     label.pack()
  #      next_button.config(text="Finish") 
    # Change button text on the last page
 #   else:
#        window.destroy()  # Close the window after the last page

# Create the main window
# Start with the first page
#current_page = 0
#show_next_content()  # Display the initial content
