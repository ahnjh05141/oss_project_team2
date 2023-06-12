from tkinter import *

import os
import sys
import pathlib
import shutil

from gitManagement import Git, Repository, Branch


root = Tk()
root.title('File Manager')
root.geometry("500x300")
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(2, weight=1)

path_gitData = os.path.join(os.getcwd(), "gitData") # git Restore을 위해 백업파일을 저장하는 폴더(gitData)의 위치

if os.path.exists(path_gitData):
    shutil.rmtree(path_gitData) # gitData를 제거 후
os.mkdir("gitData") # 다시 생성(gitData의 백업 파일을 초기화 하는 기능)

ModifiedTime = {}

# File Managing Methods ----------------------------------------------------------------------------------

def removeIcon(picked):
    icons = ["📄", "📁", "ⓤ", "ⓜ", "ⓢ", "ⓒ"]
    for icon in icons:
        picked = picked.strip(icon)
    return picked


def pathChange(*event):
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath.get())
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list
    for file in directory:
        path = os.path.join(currentPath.get(), file)

        if os.path.isfile(path):
            try:
                time = os.path.getmtime(path)
                if time != ModifiedTime[file] and Git.get_current_repo().get_current_branch().get_status(file) != 'restored':
                    Git.gitModified(file)
                    ModifiedTime[file] = time
            except:
                pass

        if os.path.isfile(path):
            if file is not None and Git.get_current_repo():
                status = Git.get_current_repo().get_current_branch().get_status(file)

                if status == "unmodified":
                    icon = "ⓤ"
                elif status == "modified":
                    icon = "ⓜ"
                elif status == "staged":
                    icon = "ⓢ"
                elif status == "committed":
                    icon = "ⓒ"

                else:
                    icon = "📄"  # file icon
            else:
                icon = "📄"  # file icon
            filetype = "." + file.split(".")[-1]  # get file extension
        elif os.path.isdir(path):
            icon = "📁"  # folder icon
            filetype = ""  # no file type for folders
        list.insert(END, f"{icon}{file}")


def changePathByClick(event=None):      # open
    try:
        picked = removeIcon(list.get(list.curselection()[0]))
        path = os.path.join(currentPath.get(), picked)
        
        if os.path.isfile(path):
            time = os.path.getmtime(path)
            ModifiedTime[picked] = time
            
            os.system("start "+ path)
        else:
            currentPath.set(path)
    except:
        print("Please select your file first\n")
        

def goBack(event=None):
    newPath = pathlib.Path(currentPath.get()).parent
    currentPath.set(newPath)


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
        os.rename(path, newname)
        top.destroy()
        pathChange('')
    except:
        print("Please select your file first\n")
        

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


# GIT Command Methods ----------------------------------------------------------------------

def git(command):
    if command == 'help':
        print("git help")
        
    elif command == 'status':
        Git.gitStatus()
        
    elif command == 'init':
        Git.gitInit(currentPath.get())                              ### Test Code, Please Edit This Line.
        
    elif command.startswith('add '):
        file = command.split('add ')[1]
        Git.gitAdd(file)
        
    elif command.startswith('restore '):
        file = command.split('restore ')[1]
        Git.gitRestore(file)
        
    elif command.startswith('rm '):
        if command.startswith('rm --cached '):
            file = command.split('rm --cached ')[1]
            Git.gitRMCached(file, currentPath.get())
        else:
            file = command.split('rm ')[1]
            Git.gitRM(file, currentPath.get())

    elif command.startswith('mv '):
        file_newname = command.split('mv ')[1]
        Git.gitMV(file_newname)
        
    elif command.startswith('commit '):
        file_message = command.split('commit ')[1]
        Git.gitCommit(file_message)
        
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




# Git Click Commands

def gitStatusClick(*event):
    Git.gitStatus()

def gitInitClick(*event):
    file = list.get(list.curselection()[0])
    path = os.path.join(currentPath.get(), removeIcon(file))
    Git.gitInit(path)

def gitAddClick(*event):
    try:
        file = list.get(list.curselection()[0])
        Git.gitAdd(removeIcon(file))
    except:
        print("\nPlease choose a file first \n")

def gitRestoreClick(*event):
    try:
        file = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), removeIcon(file))
        Git.gitRestore(removeIcon(file), path)
    except:
        print("\nPlease choose a file first \n")

def gitRMClick(*event):
    try:
        file = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), removeIcon(file))
        Git.gitRM(removeIcon(file),path)
    except:
        print("\nPlease choose a file first \n")

def gitRMCachedClick(*event):
    try:
        file = list.get(list.curselection()[0])
        Git.gitRMCached(removeIcon(file))
    except:
        print("\nPlease choose a file first \n")

def gitMVClick(*event):
    if Git.get_current_repo() and Git.get_current_repo().get_current_branch():
        newname = str(input("new name : "))
        try:
            file = list.get(list.curselection()[0])
            Git.gitMV(removeIcon(file)+" "+newname)
        except:
            print("\nPlease choose a file first \n")
    else:
        print("\nMake repository first \n")
        return

def gitCommitClick(*event):
    if Git.get_current_repo() and Git.get_current_repo().get_current_branch():
        message = str(input("commit message : "))
        try:
            file = list.get(list.curselection()[0])
            Git.gitCommit(removeIcon(file)+" -m \""+message+"\"")
        except:
            directory = os.listdir(currentPath.get())
            for file in directory:
                Git.gitCommit(removeIcon(file)+" -m \""+message+"\"")
    else:
        print("\nMake repository first \n")
        return
    
def branchCreateClick(*event):
    repo = Git.get_current_repo()
    if repo:
        name = str(input("branch name : "))
        pathChange('')
        repo.create_branch(name, currentPath.get())
    else:
        print("\nMake repository first \n")
        return
    
def branchDeleteClick(*event):
    repo = Git.get_current_repo()
    if repo:
        name = str(input("branch name for delete : "))
        repo.delete_branch(name)
    else:
        print("\nMake repository first \n")
        return
    
def branchRenameClick(*event):
    repo = Git.get_current_repo()
    if repo:
        newname = str(input("new branch name : "))
        repo.rename_branch(newname)
    else:
        print("\nMake repository first \n")
        return

def branchCheckoutClick(*event):
    repo = Git.get_current_repo()
    if repo:
        name = str(input("branch name : "))
        repo.checkout_branch(name)
    else:
        print("\nMake repository first \n")
        return

def branchShowClick(*event):
    repo = Git.get_current_repo()
    if repo:
        repo.display_branches()
    else:
        print("\nMake repository first \n")
        return


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

# File Menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Create", command=createFileOrFolder)
file_menu.add_command(label="Open", command=changePathByClick)
file_menu.add_command(label="Rename", command=renameFileOrFolder)
file_menu.add_command(label="Duplicate", command=duplicateFileOrFolder)
file_menu.add_command(label="Remove (Delete)", command=removeFileOrFolder)
file_menu.add_command(label="Refresh (F5)", command=pathChange)
file_menu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

# Repository Menu
# repository_menu = Menu(menubar, tearoff=0)
# repository_menu.add_command(label="Create", command=)
# repository_menu.add_command(label="Delete", command=)
# repository_menu.add_separator()
# repository_menu.add_command(label="Settings", command=)

# Branch Menu
branch_menu = Menu(menubar, tearoff=0)
branch_menu.add_command(label="Create", command=branchCreateClick)           # Test Code, Please Edit This Line.
branch_menu.add_command(label="Delete", command=branchDeleteClick)           # Test Code, Please Edit This Line.
branch_menu.add_command(label="Rename", command=branchRenameClick)           # Test Code, Please Edit This Line.
branch_menu.add_command(label="Checkout", command=branchCheckoutClick)           # Test Code, Please Edit This Line.
branch_menu.add_separator()
branch_menu.add_command(label="Show", command=branchShowClick)           # Test Code, Please Edit This Line.
menubar.add_cascade(label="Branch", menu=branch_menu)
root.config(menu=menubar)


# Right Click Menu
menu_file = Menu(root, tearoff = 0)
menu_file.add_command(label ="Open", command = changePathByClick)
menu_file.add_command(label ="Duplicate", command = duplicateFileOrFolder)
menu_file.add_command(label ="Rename", command = renameFileOrFolder)
menu_file.add_command(label ="Delete", command = removeFileOrFolder)
menu_file.add_separator()
menu_file.add_command(label ="git init", command = gitInitClick)
menu_file.add_separator()
menu_file.add_command(label ="git status", command = gitStatusClick)
menu_file.add_separator()
menu_file.add_command(label ="git add", command = gitAddClick)
menu_file.add_command(label ="git restore", command = gitRestoreClick)
menu_file.add_command(label ="git remove", command = gitRMClick)
menu_file.add_command(label ="git remove --cached", command = gitRMCachedClick)
menu_file.add_command(label ="git move", command = gitMVClick)
menu_file.add_separator()
menu_file.add_command(label ="git commit (selected file)", command = gitCommitClick)

menu_empty = Menu(root, tearoff = 0)
menu_empty.add_command(label ="Create", command = createFileOrFolder)
menu_empty.add_command(label ="Refresh", command = pathChange)
menu_empty.add_separator()
menu_empty.add_command(label ="git status (this repo)", command = gitStatusClick)
menu_empty.add_separator()
menu_empty.add_command(label ="git init (this folder)", command = gitInitClick)
menu_empty.add_command(label ="git commit (whole folder)", command = gitCommitClick)
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

print(" < GIT File Manager > v.1.4 \n")
pathChange('')
root.mainloop()
