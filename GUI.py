from tools.MainWindow import *
from tkinter import Label
from PIL import Image, ImageTk

#Instantiate the root of the program
root = Root()
#Instantiate main widget
main_widget = MainWidget(root.root, size=(1300, 800))
#Remove the title bar on the main widget 
main_widget.main.overrideredirect(True)
#Instantiate the custom titlebar
x_image = Label(image='')
title_bar = Title_Bar(master=main_widget, color='#2B2B2B', height=30)

root.root.mainloop()