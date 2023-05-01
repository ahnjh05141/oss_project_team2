class gitRepository:
    dirName = ""
    unmodified =  []
    modified = []
    staged = []
    committed = []

    def __init__(self, name):
        self.dirName = name


def gitRepositoryCreation(os, currentPath, repo):    #현재 Path를 인풋값으로 작동
    #이 서비스는 모든 로컬 디렉터리를 깃 저장소로 전환할 수 있도록 지원합니다.

    # Get all Files and Folders from the given Directory
    listOfFile = os.listdir(currentPath)
    for i, item in enumerate(listOfFile):
        if len(item.split('.')) != 1:    # 파일 이름을 확인 - 파일일 경우
            print(item)
            repo.unmodified.append(item)
        else:    # 파일 이름을 확인 - 폴더일 경우
            print(item)
            gitRepositoryCreation(os, currentPath + "\\" + item, repo)    #재귀

    print(repo)


def gitAdd(file, repo):    # git add
    repo.staged.append(file)    #staged에 넣음
    if file in repo.modified:    #(modified -> staged;인 경우, modified에서도 삭제해야함
        repo.modified.remove(file)

def gitRestore(file, repo):    # git restore
    if file in repo.modified:    #modified -> unmodified;인 경우
        repo.modified.remove(file)
        repo.unmodified.append(file)
        # TODO file의 상태를 수정 전으로 복구하는 작업 추가 필요
    elif file in repo.staged:    #staged -> modified or untracked;인 경우 -> git restore --staged
        repo.staged.remove(file)
        repo.modified.append(file)    #일단 modified로 넣음. 이걸 구분하는 건 없길래

def gitRM(file, repo):    # git rm
    #committed -> staged;
    repo.committed.remove(file)
    repo.staged.append(file)

def gitRMCached(file, repo):    # git rm --cached
    #committed -> untracked;
    repo.committed.remove(file)


def gitMV(file, repo):    # git mv
    #committed -> staged;
    repo.committed.remove(file)
    repo.staged.append(file)

def gitCommit(file, repo):    # git commit
    repo.staged.remove(file)
    repo.committed.append(file)
