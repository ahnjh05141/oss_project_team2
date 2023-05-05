from tkinter import *
import os
import sys
import ctypes
import pathlib
import shutil
import gitRepository

repoDict = {}    #레포지토리 객체를 value로 갖고, 폴더명을 key로 갖는 딕셔너리

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
    parentFile = currentPath.get().split('\\')[-1]
    for file in directory:
        if False:
        #if parentFile in repoDict.keys():
            repo = repoDict[parentFile]
            match gitRepository.checkStatus(file, repo):
                case 'unmodified':
                    list.insert(0, '(u)' + file)
                case 'modified':
                    list.insert(0, '(m)' + file)
                case 'staged':
                    list.insert(0, '(s)' + file)
                case 'committed':
                    list.insert(0, '(c)' + file)
                case 'untracked':
                    list.insert(0, '(unt)' + file)
        else:
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
    

def gitInitClick():
    currentDirName = list.get(list.curselection()[0])
    path = os.path.join(currentPath.get(), currentDirName)
    print("Git Init을 시도하려는 폴더 : " + currentDirName)

    # 브라우저의 현재 디렉토리가 아직 Git에 의해 관리되지 않는 경우에만 Git 리포지토리 만들기 메뉴를 제공합니다.
    for i, item in enumerate(repoDict):
        if item.dirName == currentDirName:
            print("이미 Git에 의해 관리되고 있는 폴더입니다.")
            return

    #관리 안되고 있는 폴더일 경우, Git init
    temprepo = gitRepository.gitRepository(currentDirName)    #레포지토리 객체 생성

    #함수 실행
    gitRepository.gitRepositoryCreation(os, path, temprepo)

    #리스트에 추가
    repoDict[currentDirName] = temprepo
    print("Git Init 완료.")

def gitAddClick():
    currentDirName = list.get(list.curselection()[0])
    print("Git Add를 시도하려는 파일 : " + currentDirName)
    parentDirName = currentPath.get().split('\\')[-1]
    #함수 실행
    gitRepository.gitAdd(currentDirName, repoDict[parentDirName])

    print("Git Add 완료.")
    print(repoDict[parentDirName].staged)
    pathChange('') # 디스플레이 재호출

def gitCommitClick():
    currentDirName = list.get(list.curselection()[0])
    print("Git Commit을 시도하려는 파일 : " + currentDirName)
    parentDirName = currentPath.get().split('\\')[-1]
    #함수 실행
    gitRepository.gitCommit(currentDirName, repoDict[parentDirName])

def gitUndoClick():
    currentDirName = list.get(list.curselection()[0])
    print("Git Undo를 시도하려는 파일 : " + currentDirName)
    parentDirName = currentPath.get().split('\\')[-1]
    #함수 실행
    gitRepository.gitRestore(currentDirName, repoDict[parentDirName])

def gitDeleteClick():
    currentDirName = list.get(list.curselection()[0])
    print("Git Delete를 시도하려는 파일 : " + currentDirName)
    parentDirName = currentPath.get().split('\\')[-1]
    #함수 실행
    gitRepository.gitRM(currentDirName, repoDict[parentDirName])

def gitUntrackClick():
    currentDirName = list.get(list.curselection()[0])
    print("Git Untrack을 시도하려는 파일 : " + currentDirName)
    parentDirName = currentPath.get().split('\\')[-1]
    #함수 실행
    gitRepository.gitRMCached(currentDirName, repoDict[parentDirName])

def gitRenameClick():
    currentDirName = list.get(list.curselection()[0])
    print("Git Rename을 시도하려는 파일 : " + currentDirName)
    parentDirName = currentPath.get().split('\\')[-1]
    #함수 실행
    gitRepository.gitMV(currentDirName, repoDict[parentDirName])

def gitModifiedClick():
    currentDirName = list.get(list.curselection()[0])
    print("Git Modified를 시도하려는 파일 : " + currentDirName)
    parentDirName = currentPath.get().split('\\')[-1]
    #함수 실행
    gitRepository.gitModified(currentDirName, repoDict[parentDirName])


m = Menu(root, tearoff = 0)
m.add_command(label ="Open", command = changePathByClick)
m.add_command(label ="Duplicate", command = duplicateFileOrFolder)
m.add_command(label ="Rename", command = renameFileOrFolder)
m.add_command(label ="Delete", command = removeFileOrFolder)
m.add_separator()


def menu():
    m.add_command(label ="Git Init", command = gitInitClick)

def menuUntracked():
    m.add_command(label ="Add", command = gitAddClick)

def menuUnmodified():
    m.add_command(label ="Add", command = gitAddClick)
    m.add_command(label ="Modified", command = gitModifiedClick)

def menuModified():
    m.add_command(label ="Add", command = gitAddClick)
    m.add_command(label ="Undo", command = gitUndoClick)

def menuStaged():
    m.add_command(label ="Commit", command = gitCommitClick)
    m.add_command(label ="Undo", command = gitUndoClick)

def menuCommitted():
    m.add_command(label ="Delete", command = gitDeleteClick)
    m.add_command(label ="Untrack", command = gitUntrackClick)
    m.add_command(label ="Rename", command = gitRenameClick)


def menuAdd():
    file = list.get(list.curselection()[0])
    parentFile = currentPath.get().split('\\')[-1]
    if parentFile in repoDict.keys():
        repo = repoDict[parentFile]
        match gitRepository.checkStatus(file, repo):
            case 'unmodified':
                menuUnmodified()
            case 'modified':
                menuModified()
            case 'staged':
                menuStaged()
            case 'committed':
                menuCommitted()
            case 'untracked':
                menuUntracked()
    else:
        menu()

#menuAdd()

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
