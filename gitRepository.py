from distutils.dir_util import copy_tree

class gitRepository:
    dirName = ""
    untracked = []
    unmodified =  []
    modified = []
    staged = []
    committed = []

    def __init__(self, name):
        self.dirName = name

def whichStatus(file, repo):
    if file in repo.unmodified:
        return "unmodified"
    elif file in repo.modified:
        return "modified"
    elif file in repo.staged:
        return "staged"
    elif file in repo.committed:
        return "committed"
    elif file in repo.untracked:
        return "untracked"
    else:
        return "not_exists"   

def initRecursion(os, currentPath, repo):
    # 이 서비스는 모든 로컬 디렉터리를 깃 저장소로 전환할 수 있도록 지원합니다.
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath)
    for file in directory:
        if len(file.split('.')) != 1:    # 파일 이름을 확인 - 파일일 경우
            repo.unmodified.append(file)
        else:    # 파일 이름을 확인 - 폴더일 경우
            initRecursion(os, currentPath + "\\" + file, repo)    #재귀

def gitRepositoryCreation(os, currentPath, repo, gitData):    #현재 Path를 인풋값으로 작동
    copy_tree(currentPath, gitData) # init 시에 해당 디렉토리의 모든 폴더,파일을 백업 폴더에 저장
    initRecursion(os, currentPath, repo)

def gitAdd(file, repo):    # git add
    repo.staged.append(file)    #staged에 넣음
    if file in repo.modified:    #(modified -> staged;인 경우, modified에서 삭제
        repo.modified.remove(file)
    elif file in repo.unmodified:   #(unmodified -> staged;인 경우, unmodified에서 삭제
        repo.unmodified.remove(file)
    else:                           #(untracked -> staged;인 경우, untracked에서 삭제
        repo.untracked.remove(file)

def gitRestore(file, repo):    # git restore
    if file in repo.modified:    #modified -> unmodified;인 경우
        repo.modified.remove(file)
        repo.unmodified.append(file)
    elif file in repo.staged:    #staged -> modified or untracked;인 경우 -> git restore --staged
        repo.staged.remove(file)
        repo.modified.append(file)    #일단 modified로 넣음. 이걸 구분하는 건 없길래

def gitRM(file, repo):    # git rm
    #any status -> staged;
    if file in repo.unmodified:
        repo.unmodified.remove(file)
        repo.staged.append(file)
    elif file in repo.modified:
        repo.modified.remove(file)
        repo.staged.append(file)
    elif file in repo.committed:
        repo.committed.remove(file)
        repo.staged.append(file)

def gitRMCached(file, repo):    # git rm --cached
    #any status -> staged;
    if file in repo.unmodified:
        repo.unmodified.remove(file)
        repo.staged.append(file)
    elif file in repo.modified:
        repo.modified.remove(file)
        repo.staged.append(file)
    elif file in repo.committed:
        repo.committed.remove(file)
        repo.staged.append(file)

def gitMV(file, newfile, repo):    # git mv
    #committed -> staged;
    repo.committed.remove(file)
    repo.staged.append(newfile)

def gitCommit(file, repo):    # git commit
    repo.staged.remove(file)
    repo.committed.append(file)

def gitModified(file, repo):
    if file in repo.unmodified:
        repo.unmodified.remove(file)
        repo.modified.append(file)
    elif file in repo.committed:
        repo.committed.remove(file)
        repo.modified.append(file)