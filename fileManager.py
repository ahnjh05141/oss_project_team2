from tkinter import *
import os
import sys
import ctypes
import pathlib
import shutil

root = Tk()
root.title('File Manager')
root.geometry("800x500")
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(2, weight=1)

def pathChange(*event):
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath.get())
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list
    for file in directory:
        list.insert(0, file)

def changePathByClick(event=None):
    # Get clicked item.
    try : 
        picked = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), picked)
        # Check if item is file, then open it
        if os.path.isfile(path):
            print('Opening: '+path)
            os.system("start "+ path)
        # Set new path, will trigger pathChange function.
        else:
            currentPath.set(path)
    except:
        print("Please select your file first")
        

def goBack(event=None):
    # get the new path
    newPath = pathlib.Path(currentPath.get()).parent
    # set it to currentPath
    currentPath.set(newPath)
    # simple message
    print('Going Back')


def createFileOrFolder():
    global top
    top = Toplevel(root)
    top.geometry("250x100")
    top.resizable(False, False)
    top.title("Create")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter File or Folder name').grid()
    Entry(top, textvariable=newFileName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Create", command=newFileOrFolder).grid(pady=10, sticky='NSEW')

def newFileOrFolder():
    # check if it is a file name or a folder
    if len(newFileName.get().split('.')) != 1:
        open(os.path.join(currentPath.get(), newFileName.get()), 'w').close()
    else:
        os.mkdir(os.path.join(currentPath.get(), newFileName.get()))
    # destroy the top
    top.destroy()
    pathChange('')


def renameFileOrFolder():
    global top
    top = Toplevel(root)
    top.geometry("250x100")
    top.resizable(False, False)
    top.title("Rename")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter File or Folder name').grid()
    Entry(top, textvariable=newFileName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Rename", command=renFileOrFolder).grid(pady=10, sticky='NSEW')

def renFileOrFolder():
    try:
        picked = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), picked)
        arr = path.split('\\')
        arr[len(arr)-1] = newFileName.get()
        newname = ''
        for i in arr:
            newname = newname + i + '\\'
        print (newname)
        os.rename(path, newname)
        top.destroy()
        pathChange('')
    except:
        print("Please select your file first")
        

def duplicateFileOrFolder():
    picked = list.get(list.curselection()[0])
    path = os.path.join(currentPath.get(), picked)
    if len(picked.split('.')) == 1:
        shutil.copytree(picked, (picked + "_copied"))
    else:
        arr = path.split('.')
        newfile = arr[0]+"_copied."+arr[1]
        shutil.copy(path, newfile)   
    pathChange('')
    
    #shutil.copy(path)


def removeFileOrFolder():
    picked = list.get(list.curselection()[0])
    path = os.path.join(currentPath.get(), picked)
    try:
        os.remove(path)
    except:
        try: 
            os.rmdir(path)
        except:
            print("Please empty your folder")
    pathChange('')
    

def emptyCommand():
    print("emptyCommand")
    

m = Menu(root, tearoff = 0)
m.add_command(label ="Open", command = changePathByClick)
m.add_command(label ="Duplicate", command = duplicateFileOrFolder)
m.add_command(label ="Duplicate", command = renameFileOrFolder)
m.add_separator()
m.add_command(label ="Delete", command = removeFileOrFolder)
m.add_separator()
m.add_command(label ="Git", command = emptyCommand)
m.add_command(label ="Add", command = emptyCommand)
m.add_command(label ="Commit", command = emptyCommand)
m.add_separator()
m.add_command(label ="Push", command = emptyCommand)


def right_click(event):
    try:
        picked = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), picked)
        print(picked)
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()
    except:
        print("Please select your file first")
    
  
root.bind("<Button-3>", right_click)





top = ''

# String variables
newFileName = StringVar(root, "File.dot", 'new_name')
currentPath = StringVar(
    root,
    name='currentPath',
    value=pathlib.Path.cwd()
)
# Bind changes in this variable to the pathChange function
currentPath.trace('w', pathChange)

Button(root, text='Back', command=goBack).grid(
    sticky='NSEW', column=0, row=0
)

# Keyboard shortcut for going up
root.bind("<Alt-Up>", goBack)

Entry(root, textvariable=currentPath).grid(
    sticky='NSEW', column=1, row=0, columnspan=2, ipady=5, ipadx=10
)

# List of files and folder
list = Listbox(root)
list.grid(sticky='NSEW', column=1, row=2, columnspan=2, ipady=10, ipadx=10)

# List Accelerators
list.bind('<Double-1>', changePathByClick)
list.bind('<Return>', changePathByClick)


# Menu
menubar = Menu(root)
menubar.add_command(label="Create", command=createFileOrFolder)
menubar.add_command(label="Open", command=changePathByClick)
menubar.add_command(label="Rename", command=renameFileOrFolder)
menubar.add_command(label="Duplicate", command=duplicateFileOrFolder)
menubar.add_command(label="Delete", command=removeFileOrFolder)
menubar.add_command(label="Refresh", command=pathChange)
menubar.add_command(label="Quit", command=root.quit)

root.config(menu=menubar)

# Call the function so the list displays
pathChange('')
# run the main program
root.mainloop()
