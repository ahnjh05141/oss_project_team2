class gitRepository:
    dirName = ""
    unmodified =  []
    modified = []
    staged = []
    committed = []

    def __init__(self, name):
        self.dirName = name


def gitRepositoryCreation(os, currentPath, repo):    #현재Path를 인풋값으로 작동
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

