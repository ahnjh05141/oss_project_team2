from tkinter import *
import os
import sys
import ctypes
import pathlib
import shutil
import gitRepository
import clone


# GUI Skeleton

root = Tk()
root.title('File Manager')
root.geometry("500x300")
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(2, weight=1)

path_gitData = os.path.join(os.getcwd(), "gitData") # git Restore을 위해 백업파일을 저장하는 폴더(gitData)의 위치
shutil.rmtree(path_gitData) # gitData를 제거 후
os.mkdir("gitData") # 다시 생성(gitData의 백업 파일을 초기화 하는 기능)

repos = []
commits = {}
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
                if time != ModifiedTime[file] and not gitRepository.isRestored(file, repos[findMasterBranch()][0]):
                    gitModified(file)
                    ModifiedTime[file] = time
            except:
                pass

        if os.path.isfile(path):
            if file is not None and len(repos) != 0:
                status = checkStatus(file, repos[findMasterBranch()][0])

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




# Git repo skeleton => repos[ [REPO_OBJECT, path, name, branch, message] , [], ... ]


def findMasterBranch():
    for i in range(0, len(repos)):
        if repos[i][3] == "MASTER":
            return i

def checkStatus(file, repo):
    return gitRepository.whichStatus(file, repo)    


# GIT Command Methods ----------------------------------------------------------------------

def gitStatus():
    pathChange('')
    try:
        repo = repos[findMasterBranch()][0]
        print("==================================================================")
        print("Current WorkSpace :", repo.dirName)
        print("* Commits :",str(commits).replace('[', '').replace(']', '').replace('\'', ''))
        print("\nUnmodified Files :",str(repo.unmodified).replace('\'',''))
        print("Modified Files :",str(repo.modified).replace('\'',''))
        print("Staged Files :",str(repo.staged).replace('\'',''))
        print("Committed Files :",str(repo.committed).replace('\'',''))
        print("==================================================================\n")
        
    except:
        print("\nMake repository first \n")
        return

def gitAdd(file):
    try:
        status = checkStatus(file, repos[findMasterBranch()][0])
    except:
        print("\nMake repository first \n")
        return
    
    if status == "not_exists":
        print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2])
    else:
        gitRepository.gitAdd(file, repos[findMasterBranch()][0])
        print("\n", file, " Successfully added \n")
        

def gitRestore(file,path):
    try:
        status = checkStatus(file, repos[findMasterBranch()][0])
    except:
        print("\nMake repository first \n")
        return
    
    if status == "not_exists":
        print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2])
    elif status == "modified" or status == "staged":
        gitRepository.gitRestore(file, repos[findMasterBranch()][0])
        path_repo = repos[findMasterBranch()][1] # 레포의 디렉토리
        path_subroot = path[len(path_repo):] # 레포에서 해당 폴더까지 도달하는 중간 과정
        path_duplicate = path_gitData + path_subroot # gitData에 저장된 복제본의 위치
        os.remove(path) # 로컬에서 지우고
        shutil.copy2(path_duplicate, path) # 백업에서 로컬로 복제
        print("\n", file, " Successfully restored \n")
    else:
        print("\nThere is no modified or staged file called [", file, "]")
        

def gitRM(file, path):
    try:
        status = checkStatus(file, repos[findMasterBranch()][0])
    except:
        print("\nMake repository first \n")
        return

    if status == "not_exists":
        print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2],"\n")
    elif status == "untracked":
        print("\nThere is no tracked file called [", file, "]")
    else:
        gitRepository.gitRM(file, repos[findMasterBranch()][0])
        os.remove(path)
        print("\n", file, " Successfully staged remove \n")


def gitRMCached(file):
    try:
        status = checkStatus(file, repos[findMasterBranch()][0])
        print(status)
    except:
        print("\nMake repository first \n")
        return
    
    if status == "not_exists":
        print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2],"\n")
    elif status == "untracked":
        print("\nThere is no tracked file called [", file, "]")
    else:
        gitRepository.gitRMCached(file, repos[findMasterBranch()][0])
        print("\n", file, " Successfully staged remove \n")


def gitMV(file_newname):
    if len(repos) > 0:
        try:
            file = file_newname.split(' ')[0]
            newname = file_newname.split(' ')[1]
            path = os.path.join(currentPath.get(), file)
            newpath = os.path.join(currentPath.get(), newname)
        except:
            print("\nWrong Command\n")
            return
        
        try:
            status = checkStatus(file, repos[findMasterBranch()][0])
        except:
            print("\nMake repository first \n")
            return

        if status == "not_exists":
            print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2],"\n")
        elif status == "committed":
                os.rename(path, newpath)
                pathChange('')
                gitRepository.gitMV(file, newname, repos[findMasterBranch()][0])
                print("\n", file, " Successfully renamed to staging area \n")
        else:
            print("\nThere is no commited file called [", file, "]")
    else:
        print("\nMake repository first \n")
        return

def gitCommit(file_message):
    if len(repos) > 0:
        try:
            file = file_message.split('-m ')[0].replace(' ', '')
            message = file_message.split('-m ')[1]

        except:
            file = file_message.replace(' ', '')
            message = ""
            
        try:
            status = checkStatus(file, repos[findMasterBranch()][0])
        except:
            print("\nMake repository first \n")
            return
        
        if status == "not_exists":
            print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2])
        elif status == "staged":
            if message == "":
                print("\nPlesase enter commit message \n")
                return
            else:
                gitRepository.gitCommit(file, repos[findMasterBranch()][0])
                commits[message] = repos[findMasterBranch()][0].committed
                print("\n", file, " Successfully committed with message", message, "\n")
                gitStatus()
        else:
            print("\nThere is no staged file called [", file, "] in staging area")
    else:
        print("\nMake repository first \n")
        return
 

def gitModified(file):
    try:
        status = checkStatus(file, repos[findMasterBranch()][0])
    except:
        print("\nMake repository first \n")
        return
    
    try:
        gitRepository.gitModified(file, repos[findMasterBranch()][0])
        print(file, "has been Modified\n")
    except:
        print("\nThere is no file called [", file, "] in directory :", repos[findMasterBranch()][2])



def gitInit(path):
    currentDirName = path.split('\\')[-1]
           
    for i in range(0, len(repos)):
        if currentDirName in repos[i][2]:       # 현재 경로와 레포에 추가돼있는 경로를 비교하여 중복을 방지
            print("\nRepository already exists :", currentDirName, "\n")
            return

    temprepo = gitRepository.gitRepository(currentDirName)    # 레포 객체 생성
    temprepo.dirName = currentDirName

    gitRepository.gitRepositoryCreation(os, path, temprepo, path_gitData)


    if len(repos) == 0:         # 처음 만든 레포라면, 마스터 브랜치를 달아주자
        branch = "MASTER"
    else:
        branch = ""

    message = ""
    repos.append([temprepo, path, currentDirName, branch, message])    # 레포 리스트에 추가

    print("\n* New Git Repo :", path, "- ("+branch+")")
    gitStatus()
    


def git(command):
    if command == 'help':
        print("git help")
        
    elif command == 'status':
        gitStatus()
        
    elif command == 'init':
        gitInit(currentPath.get())
        
    elif command.startswith('add '):
        file = command.split('add ')[1]
        gitAdd(file)
        
    elif command.startswith('restore '):
        file = command.split('restore ')[1]
        gitRestore(file)
        
    elif command.startswith('rm '):
        if command.startswith('rm --cached '):
            file = command.split('rm --cached ')[1]
            gitRMCached(file)
        else:
            file = command.split('rm ')[1]
            gitRM(file)

    elif command.startswith('mv '):
        file_newname = command.split('mv ')[1]
        gitMV(file_newname)
        
    elif command.startswith('commit '):
        file_message = command.split('commit ')[1]
        gitCommit(file_message)
        
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

def clonePublicClick(*event):
    print("Enter GitHub address (https://~~~.git)")
    address = input()
    file = list.get(list.curselection()[0])
    local = os.path.join(currentPath.get(), removeIcon(file))
    clone.clone_public(local, address)

def clonePrivateClick(*event):
    print("Enter GitHub address (https://~~~.git)")
    address = input()
    print("Enter the ID")
    id = input()
    print("Enter the token (PAT)")
    token = input()
    file = list.get(list.curselection()[0])
    local = os.path.join(currentPath.get(), removeIcon(file))
    clone.clone_private(local, address, id)
    clone.store(address, id, token)

def gitStatusClick(*event):
    gitStatus()

def gitInitClick(*event):
    file = list.get(list.curselection()[0])
    path = os.path.join(currentPath.get(), removeIcon(file))
    gitInit(path)

def gitAddClick(*event):
    try:
        file = list.get(list.curselection()[0])
        gitAdd(removeIcon(file))
    except:
        print("\nPlease choose a file first \n")

def gitRestoreClick(*event):
    try:
        file = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), removeIcon(file))
        gitRestore(removeIcon(file),path)
    except:
        print("\nPlease choose a file first \n")

def gitRMClick(*event):
    try:
        file = list.get(list.curselection()[0])
        path = os.path.join(currentPath.get(), removeIcon(file))
        gitRM(removeIcon(file),path)
    except:
        print("\nPlease choose a file first \n")

def gitRMCachedClick(*event):
    try:
        file = list.get(list.curselection()[0])
        gitRMCached(removeIcon(file))
    except:
        print("\nPlease choose a file first \n")

def gitMVClick(*event):
    if len(repos) > 0:
        newname = str(input("new name : "))
        try:
            file = list.get(list.curselection()[0])
            gitMV(removeIcon(file)+" "+newname)
        except:
            print("\nPlease choose a file first \n")
    else:
        print("\nMake repository first \n")
        return

def gitCommitClick(*event):
    if len(repos) > 0:
        message = str(input("commit message : "))
        try:
            file = list.get(list.curselection()[0])
            gitCommit(removeIcon(file)+" -m \""+message+"\"")
        except:
            directory = os.listdir(currentPath.get())
            for file in directory:
                gitCommit(removeIcon(file)+" -m \""+message+"\"")
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
menubar.add_command(label="Create", command=createFileOrFolder)
menubar.add_command(label="Open", command=changePathByClick)
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
menu_file.add_command(label ="clone public repository", command = clonePublicClick)
menu_file.add_command(label ="clone private repository", command = clonePrivateClick)
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
