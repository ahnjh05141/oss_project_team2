import os

from distutils import dir_util
from shutil import rmtree, copy2, move


class Branch():
    def __init__(self, name, repoPath):
        self.branchName = name
        self.branchPath = os.path.join(repoPath, name)
        self.untracked = []
        self.unmodified = []
        self.modified = []
        self.staged = []
        self.committed = []
        self.restored = []
        self.commits = {}

        os.mkdir(self.branchPath)

    
    def gitAdd_func(self, file):
        self.staged.append(file)    #staged에 넣음
        if file in self.modified:    #(modified -> staged;인 경우, modified에서 삭제
            self.modified.remove(file)
        elif file in self.unmodified:   #(unmodified -> staged;인 경우, unmodified에서 삭제
            self.unmodified.remove(file)
        else:                           #(untracked -> staged;인 경우, untracked에서 삭제
            try:
                self.untracked.remove(file)
            except:
                pass


    def gitCommit_func(self, file):
        self.staged.remove(file)
        self.committed.append(file)


    def gitModified_func(self, file):
        if file in self.unmodified:
            self.unmodified.remove(file)
            self.modified.append(file)
        elif file in self.committed:
            self.committed.remove(file)
            self.modified.append(file)

    
    def gitMV_func(self, file, newfile):    # git mv
        #committed -> staged;
        self.committed.remove(file)
        self.staged.append(newfile)


    def gitRestore_func(self, file):        # git restore
        if file in self.modified:    #modified -> unmodified;인 경우
            self.modified.remove(file)
            self.unmodified.append(file)
            self.restored.append(file)
        elif file in self.staged:    #staged -> modified or untracked;인 경우 -> git restore --staged
            self.staged.remove(file)
            self.unmodified.append(file)    #일단 modified로 넣음. 이걸 구분하는 건 없길래
            self.restored.append(file)


    def gitRM_func(self, file):             # git rm
        #any status -> staged;
        if file in self.unmodified:
            self.unmodified.remove(file)
            self.staged.append(file)
        elif file in self.modified:
            self.modified.remove(file)
            self.staged.append(file)
        elif file in self.committed:
            self.committed.remove(file)
            self.staged.append(file)


    def gitRMCached_func(self, file):       # git rm --cached
        #any status -> staged;
        if file in self.unmodified:
            self.unmodified.remove(file)
            self.staged.append(file)
        elif file in self.modified:
            self.modified.remove(file)
            self.staged.append(file)
        elif file in self.committed:
            self.committed.remove(file)
            self.staged.append(file)


    def get_status(self, file) -> str :
        if file in self.untracked:
            return "untracked"
        if file in self.unmodified:
            return "unmodified"
        if file in self.modified:
            return "modified"
        if file in self.staged:
            return "staged"
        if file in self.committed:
            return "comitted"
        if file in self.restored:
            return "restored"
        
        return "not_exists"



class Repository():
    def __init__(self, name, path):
        self.repoName = name
        self.repoPath = os.path.join(Git.path_gitData, name)
        self.branches = []
        self.current_branch = ""

        os.mkdir(self.repoPath)
        self.create_branch('MASTER', path)

    # Create Branch
    def create_branch(self, name, path):
        if self.get_branch(name):
            print(f"Branch '{name}' already exists.\n")
        else:
            branch = Branch(name, self.repoPath)
            self.branches.append(branch)
            try:
                Git.init_recursion(path, branch)
                dir_util.copy_tree(path, branch.branchPath)
            except:
                pass
            self.current_branch = name
            print(f"Created branch '{name}'.\n")

    # Delete Branch
    def delete_branch(self, name):
        if name == "MASTER":
            print("Cannot delete 'MASTER' branch.\n")
        else:
            branch = self.get_branch(name)
            if branch:
                rmtree(branch.branchPath)
                self.branches.remove(branch)
                print(f"Deleted branch '{name}'.\n")
                self.current_branch = "MASTER"
            else:
                print(f"Branch '{name}' does not exist.\n")

    # Rename Branch
    def rename_branch(self, name):
        branch = self.get_current_branch()
        if branch:
            print(f"Renamed branch '{branch.branchName}' to '{name}'.\n")
            branch.branchName = name
        else:
            print(f"Branch '{name}' does not exist.\n")   

    # Checkout Branch
    def checkout_branch(self, name):
        branch = self.get_branch(name)
        if branch:
            self.current_branch = branch.branchName
            print(f"Switched to branch '{name}'.\n")
        else:
            print(f"Branch '{name}' does not exist.\n")

    # Display Branches
    def display_branches(self):
        print("\n---------------------------------------------------")
        print(f"Branches in repository '{self.repoName}':\n")
        for branch in self.branches:
            print(branch.branchName)
        print(f"Current branch: {self.current_branch}")
        print("---------------------------------------------------\n")
    
    # get Branch
    def get_branch(self, name) -> Branch | None:
        for branch in self.branches:
            if branch.branchName == name:
                return branch
        return None
    
    def get_current_branch(self) -> Branch | None:
        return self.get_branch(self.current_branch)


    # Merge Branch
    def merge_branches(self, name):
        branch = self.get_branch(name)
        master_branch = self.get_branch("MASTER")
        if branch:
            if name != self.current_branch:
                print(branch.branchPath, master_branch.branchPath)
                move(branch.branchPath, master_branch.branchPath)
                self.delete_branch(name)
                print(name, "merged to MASTER")
            else:
                print("Can not merge current branch.\n")
        else:
            print(f"Branch does not exist.\n")


class Git():
    path_gitData = os.path.join(os.getcwd(), "gitData") # git Restore을 위해 백업파일을 저장하는 폴더(gitData)의 위치

    if os.path.exists(path_gitData):
        try:
            rmtree(path_gitData) # gitData를 제거 후
        except:
            pass
    os.mkdir(path_gitData) # 다시 생성(gitData의 백업 파일을 초기화 하는 기능)

    repos = []
    current_repo = ""


    def create_repository(dirName, path):
        for repo in Git.repos:
            if dirName in repo.repoName:                                # 이미 동일한 이름의 Repository가 존재할 경우
                print(f"\nRepository already exists : {dirName} \n")
                return
            
        temprepo = Repository(dirName, path)
        Git.current_repo = temprepo.repoName
        Git.repos.append(temprepo)

        Git.gitStatus()


    def init_recursion(currentPath, branch):
        directory = os.listdir(currentPath)
        for file in directory:
            if len(file.split('.')) != 1:                               # 파일 이름을 확인 - 파일일 경우
                branch.unmodified.append(file)
            else:                                                       # 파일 이름을 확인 - 폴더일 경우
                Git.init_recursion(currentPath + "\\" + file, branch)         #재귀

    # get Repository
    def get_repo(name) -> Repository | None :
        for repo in Git.repos:
            if repo.repoName == name:
                return repo
        return None 

    def get_current_repo() -> Repository | None :
        return Git.get_repo(Git.current_repo) 
    
    def gitInit(path):
        currentDirName = path.split("\\")[-1]

        Git.create_repository(currentDirName, path)

    def gitStatus():
        repo = Git.get_current_repo()
        branch = repo.get_current_branch()

        print("==================================================================")
        print("Current WorkSpace :", repo.repoName)
        print("Current Branch :", branch.branchName)
        print("* Commits :",str(branch.commits).replace('[', '').replace(']', '').replace('\'', ''))
        print("\nUnmodified Files :",str(branch.unmodified).replace('\'',''))
        print("Modified Files :",str(branch.modified).replace('\'',''))
        print("Staged Files :",str(branch.staged).replace('\'',''))
        print("Committed Files :",str(branch.committed).replace('\'',''))
        print("==================================================================\n")



    def gitAdd(file):
        repo = Git.get_current_repo()
        if repo:
            branch = repo.get_current_branch()
            if branch:
                status = branch.get_status(file)
                print(status)
            else:
                print("\nMake branch first \n")
                return
            
            if status == "not_exists":
                print("\nThere is no file called [", file, "] in directory :", repo.repoName,"\n")
            else:
                branch.gitAdd_func(file)
                print("\n", file, " Successfully added \n")
        else:
            print("\nMake repository first \n")
            return


    def gitRestore(file, path):
        repo = Git.get_current_repo()
        if repo:
            branch = repo.get_current_branch()
            if branch:
                status = branch.get_status(file)
                print(status)
            else:
                print("\nMake branch first \n")
                return
            
            if status == "not_exists":
                print("\nThere is no file called [", file, "] in directory :", repo.repoName,"\n")
            elif status == "modified" or status == "staged":
                branch.gitRestore_func(file)
                path_repo = repo.repoPath # 레포의 디렉토리
                path_subroot = path[len(path_repo):] # 레포에서 해당 폴더까지 도달하는 중간 과정
                path_duplicate = Git.path_gitData + path_subroot # gitData에 저장된 복제본의 위치
                os.remove(path) # 로컬에서 지우고
                copy2(path_duplicate, path) # 백업에서 로컬로 복제
                print("\n", file, " Successfully restored \n")
            else:
                print("\nThere is no modified or staged file called [", file, "]")
        else:
            print("\nMake repository first \n")
            return


    def gitRM(file):
        repo = Git.get_current_repo()
        if repo:
            branch = repo.get_current_branch()
            if branch:
                status = branch.get_status(file)
                print(status)
            else:
                print("\nMake branch first \n")
                return
            
            if status == "not_exists":
                print("\nThere is no file called [", file, "] in directory :", repo.repoName,"\n")
            elif status == "untracked":
                print("\nThere is no tracked file called [", file, "]")
            else:
                branch.gitRM_func(file)
                print("\n", file, " Successfully staged remove \n")
        else:
            print("\nMake repository first \n")
            return


    def gitRMCached(file):
        repo = Git.get_current_repo()
        if repo:
            branch = repo.get_current_branch()
            if branch:
                status = branch.get_status(file)
                print(status)
            else:
                print("\nMake branch first \n")
                return
            
            if status == "not_exists":
                print("\nThere is no file called [", file, "] in directory :", repo.repoName,"\n")
            elif status == "untracked":
                print("\nThere is no tracked file called [", file, "]")
            else:
                branch.gitRMCached_func(file)
                print("\n", file, " Successfully staged remove \n")
        else:
            print("\nMake repository first \n")
            return


    def gitMV(file_newname, currentPath):
        repo = Git.get_current_repo()
        if repo:
            branch = repo.get_current_branch()
            if branch:
                try:
                    file = file_newname.split(' ')[0]
                    newname = file_newname.split(' ')[1]
                    path = os.path.join(currentPath, file)
                    newpath = os.path.join(currentPath, newname)
                except:
                    print("\nWrong Command\n")
                    return
                
                
                status = branch.get_status(file)

                if status == "not_exists":
                    print("\nThere is no file called [", file, "] in directory :", repo.repoName,"\n")
                elif status == "committed":
                        os.rename(path, newpath)
                        # pathChange('')                                                    # Test Code, Please Edit This Line.
                        branch.gitMV_func(file, newname)
                        print("\n", file, " Successfully renamed to staging area \n")
                else:
                    print("\nThere is no commited file called [", file, "]")
            else:
                print("\nMake branch first \n")
        else:
            print("\nMake repository first \n")
            return


    def gitCommit(file_message):
        repo = Git.get_current_repo()
        if repo:
            branch = repo.get_current_branch()
            if branch:
                try:
                    file = file_message.split('-m ')[0].replace(' ', '')
                    message = file_message.split('-m ')[1]
                except:
                    file = file_message.replace(' ', '')
                    message = ""
                    
                try:
                    status = branch.get_status(file)
                except:
                    print("\nMake branch first \n")
                    return
                
                if status == "not_exists":
                    print("\nThere is no file called [", file, "] in directory :", repo.repoName,"\n")
                elif status == "staged":
                    if message == "":
                        print("\nPlesase enter commit message \n")
                        return
                    else:
                        branch.gitCommit_func(file)
                        branch.commits[message] = branch.committed
                        print("\n", file, " Successfully committed with message", message, "\n")
                        Git.gitStatus()
                else:
                    print("\nThere is no staged file called [", file, "] in staging area")
            else:
                print("\nMake branch first \n")
        else:
            print("\nMake repository first \n")
            return


    def gitModified(file):
        try:
            repo = Git.get_current_repo()
        except:
            print("\nMake repository first \n")
            return
        
        try:
            branch = repo.get_current_branch()
            status = branch.get_status(file)
        except:
            print("\nMake branch first \n")
            return
    
        try:
            branch.gitModified_func(file)
            print(file, "has been Modified\n")
        except:
            print("\nThere is no file called [", file, "] in directory :", )
