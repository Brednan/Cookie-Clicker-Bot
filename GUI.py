from tools.MainWindow import *
from tkinter import Label, PhotoImage
from PIL import Image, ImageTk

#Instantiate the root of the program
root = Root()

#Instantiate main widget
main_widget = MainWidget(root.root, size=(1300, 800))

#Remove the title bar on the main widget 
main_widget.main.overrideredirect(True)

#Instantiate the custom titlebar
x_image = ImageTk.PhotoImage(Image.open('./resources/X_Button.png').resize((25, 25)))
title_bar = Title_Bar(master=main_widget, color='#2B2B2B', height=30, x_image=x_image)

root.root.mainloop()