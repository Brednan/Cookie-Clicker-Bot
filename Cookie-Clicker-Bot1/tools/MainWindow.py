import tkinter as tk

class Root():
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0)

class MainWidget():
    def __init__(self, root, size:tuple):
        self.size = size
        self.root = root
        self.root.bind('<Button-1>', self.focus_widget)
        self.main = tk.Toplevel(master=root, width=size[0], height=size[1])
        self.main.bind('<Button-1>', self.focus_widget)
    
    def focus_widget(self, e):
        self.main.focus_set()

class Title_Bar():
    def __init__(self, master, color, height, x_image):
        self.master = master
        self.title_bar = tk.Frame(master=master.main, bg=color, width=self.master.size[0], height=height)
        self.title_bar.place(x=0, y=0, anchor=tk.NW)
        self.title_bar.bind('<B1-Motion>', self.mouse_drag)
        
        self.x_button = tk.Button(master=self.title_bar, image=x_image, width=25, height=25)

    def mouse_drag(self, e):
        self.master.main.geometry(f'+{e.x_root}+{e.y_root}')
    