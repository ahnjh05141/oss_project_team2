from tkinter import *
import os
import sys
import ctypes
import pathlib
import shutil
import gitRepository

# GUI Skeleton

root = Tk()
root.title('File Manager')
root.geometry("800x500")
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(2, weight=1)


# File Managing Methods ----------------------------------------------------------------------------------

def removeIcon(picked):
    return picked.strip("📄").strip("📁")

def pathChange(*event):
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath.get())
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list
    for file in directory:
        # get full path
        path = os.path.join(currentPath.get(), file)
        # get icon and file type
        if os.path.isfile(path):
            icon = "📄" # file icon
            filetype = "." + file.split(".")[-1] # get file extension
        elif os.path.isdir(path):
            icon = "📁" # folder icon
            filetype = "" # no file type for folders
        # Insert file and icon into the list
        list.insert(END, f"{icon}{file}")


def changePathByClick(event=None):
    # Get clicked item.
    try : 
        picked = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), removeIcon(picked))
        
        # Check if item is file, then open it
        if os.path.isfile(path):
            print('Opening: '+path)
            os.system("start "+ path)
        # Set new path, will trigger pathChange function.
        else:
            currentPath.set(path)
    except:
        print("Please select your file first (changepathbyclick)")
        

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
        path = os.path.join(currentPath.get(), removeIcon(picked))
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
    path = os.path.join(currentPath.get(), removeIcon(picked))
    if len(picked.split('.')) == 1:
        shutil.copytree(picked, (picked + "_copied"))
    else:
        arr = path.split('.')
        newfile = arr[0]+"_copied."+arr[1]
        shutil.copy(path, newfile)   
    pathChange('')
    
    #shutil.copy(path)


def removeFileOrFolder(*event):
    picked = list.get(list.curselection()[0])
    path = os.path.join(currentPath.get(), removeIcon(picked))
    try:
        os.remove(path)
    except:
        try: 
            os.rmdir(path)
        except:
            print("Check the folder is empty!!")
    pathChange('')




# Git repo skeleton => repos[ [REPO_OBJECT], [path], [name], [branch] ]

repos = []


# GIT Command Methods ----------------------------------------------------------------------

def findMasterBranch():
    for i in range(0, len(repos)):
        if repos[i][3] == "MASTER":
            return i

def gitStatusClick():
    repos[findMasterBranch()][0].checkStatus()


def gitAddClick(file):
    try:
        gitRepository.gitAdd(file, repos[findMasterBranch()][0])
        print("\n", file, " Successfully Added \n")
    except:
        print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2])



def gitInitClick(path):
    currentDirName = path.split('\\')[-1]
           
    for i in range(0, len(repos)):
        if currentDirName in repos[i][2]:       # 현재 경로와 레포에 추가돼있는 경로를 비교하여 중복을 방지
            print("\nRepository already exists :", currentDirName, "\n")
            return

    temprepo = gitRepository.gitRepository(currentDirName)    # 레포 객체 생성
    temprepo.dirName = currentDirName

    gitRepository.gitRepositoryCreation(os, path, temprepo)



    if len(repos) == 0:         # 처음 만든 레포라면, 마스터 브랜치를 달아주자
        branch = "MASTER"
    else:
        branch = ""
        
    repos.append([temprepo, path, currentDirName, branch])    # 리스트에 추가

    print("\n* New Git Repo :", path, "- ("+branch+")")
    gitStatusClick()
    
    




def git(command):
    if command == 'help':
        print("git help")
        
    elif command == 'status':
        gitStatusClick()
        
    elif command == 'init':
        gitInitClick(currentPath.get())
        
    elif command.startswith('add '):
        file = command.split('add ')[1]
        gitAddClick(file)
        
    elif command.startswith('restore '):
        file = command.split('restore ')[1]
        print("git restore", file)
        
    elif command.startswith('rm '):
        file = command.split('rm ')[1]
        print("git rm", file)
        
    elif command.startswith('rm --cached '):
        file = command.split('rm --cached ')[1]
        print("git rm --cached", file)
        
        
    else:
        print("> Unknown GIT command [ git",command,"] found")

    
    
def runTerminalCommands(event):
    line = terminal.get()
    terminal.delete(0, len(line))
    
    if line == "":
        print('')
    else:
        print("$", line)
        
    if line.startswith('cd '):
        path = line.split('cd ')[1]
        print(path)
        

    elif line.startswith('git '):
        command = line.split('git ')[1]
        git(command)
        
    else:
        print("> Unknown command [",line,"] found")


def emptyCommand():
    print("")



# Program Components -------------------------------------------------------------------

top = ''

# String variables
newFileName = StringVar(root, "File.dot", 'new_name')

currentPath = StringVar(root, name='currentPath', value=pathlib.Path.cwd())

# Bind changes in this variable to the pathChange function
currentPath.trace('w', pathChange)

# GoBack Button
Button(root, text='Back', command=goBack).grid(sticky='NSEW', column=0, row=0)

# Shows Current Path 
Entry(root, textvariable=currentPath).grid(sticky='NSEW', column=1, row=0, columnspan=2, ipady=5, ipadx=10)

# File and Folder List
list = Listbox(root)
list.grid(sticky='NSEW', column=1, row=2, columnspan=2, ipady=10, ipadx=10)


# >
Label(root, text = ">").grid(column=0, row=3)


# Terminal Command Entry
terminal = Entry(root)
terminal.grid(sticky="NSEW", column=1, row=3, columnspan=2, ipady=10, ipadx=10)

# Menu Bar
menubar = Menu(root)
menubar.add_command(label="Create", command=createFileOrFolder)
menubar.add_command(label="Open (Enter)", command=changePathByClick)
menubar.add_command(label="Rename", command=renameFileOrFolder)
menubar.add_command(label="Duplicate", command=duplicateFileOrFolder)
menubar.add_command(label="Remove (Delete)", command=removeFileOrFolder)
menubar.add_command(label="Refresh (F5)", command=pathChange)
menubar.add_command(label="Quit", command=root.quit)

root.config(menu=menubar)


# Right Click Menu

menu_file = Menu(root, tearoff = 0)
menu_file.add_command(label ="Open", command = changePathByClick)
menu_file.add_command(label ="Duplicate", command = duplicateFileOrFolder)
menu_file.add_command(label ="Rename", command = renameFileOrFolder)
menu_file.add_command(label ="Delete", command = removeFileOrFolder)
menu_file.add_separator()
menu_file.add_command(label ="git init", command = emptyCommand)
menu_file.add_separator()
menu_file.add_command(label ="git add", command = emptyCommand)
menu_file.add_command(label ="git undo", command = emptyCommand)
menu_file.add_command(label ="git commit", command = emptyCommand)
menu_file.add_separator()
menu_file.add_command(label ="git rename", command = emptyCommand)
menu_file.add_command(label ="git untrack", command = emptyCommand)
menu_file.add_command(label ="git remove", command = emptyCommand)

menu_empty = Menu(root, tearoff = 0)
menu_empty.add_command(label ="Create", command = createFileOrFolder)
menu_empty.add_command(label ="Refresh", command = pathChange)
menu_empty.add_separator()
menu_empty.add_command(label ="Quit", command = root.quit)


# Mouse Inputs

def right_click(event):
    try: 
        picked = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), picked)
        try:
            menu_file.tk_popup(event.x_root, event.y_root)
        finally:
            menu_file.grab_release()

    except:
        try:
            menu_empty.tk_popup(event.x_root, event.y_root)
        finally:
            menu_empty.grab_release()
        
  
root.bind("<Button-3>", right_click)


# Keyboard Inputs

root.bind("<F5>", pathChange)
root.bind("<Delete>", removeFileOrFolder)

list.bind('<Double-1>', changePathByClick)

terminal.bind('<Return>', runTerminalCommands)



# Run Program ---------------------------------------------------------------------------

print("GIT File Manager v.1.2 \n")
pathChange('')
root.mainloop()
