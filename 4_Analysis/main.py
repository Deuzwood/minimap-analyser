import os
import sys


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


racine_path = get_parent_dir(1)
const_path = os.path.join(racine_path, "Const")
data_path = os.path.join(racine_path, "Data")
res_path = os.path.join(racine_path, "res")

sys.path.append(const_path)

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import const
from PIL import Image

champions_list_path = os.path.join(racine_path, const.CHAMPIONS_LIST_PATH)
champions_tile_path = os.path.join(racine_path, const.CHAMPIONS_TILE_PATH)


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


def selectFile(event=None):
    filetypes = (("csv file", "*.csv"), ("Minimap video", "*.mp4"))

    filename = fd.askopenfilename(
        title="Open a file", initialdir="/", filetypes=filetypes
    )
    f = open(filename)
    print(f.read())
    # showinfo(title="Selected File", message=filename)


def championsTile():
    load = Image.open("parrot.jpg")
    render = ImageTk.PhotoImage(load)
    img = Label(self, image=render)
    img.image = render
    img.place(x=0, y=0)


def aboutWindow():
    filewin = Toplevel(root)
    text = Text(filewin)
    text.insert(INSERT, "Version 0.1")
    text.pack()


root = Tk()
root.geometry("720x480")
root.resizable(False, False)
root.title("Minimap Analyser")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=selectFile)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=aboutWindow)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

load = Image.open(champions_tile_path + "/annie.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.place(x=0, y=0)

# keybind
root.bind("<Control-o>", selectFile)

root.mainloop()