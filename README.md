# OSS_project_team2
2023 오픈소스 SW 프로젝트 팀 프로젝트 Team 2 - 안재현, 오가은, 이태운, 최병욱

### 실행법, 실행 환경
사용 OS : Windows<br/>

Python 설치 후, 터미널에서 “python fileManager.py” 명령어를 실행

### 최종 실행화면

![최종 실행화면](https://github.com/ahnjh05141/oss_project_team2/assets/56011947/5d68eac9-0d98-4f8c-8ff5-df7281d61342)


### 참고 오픈소스
https://github.com/x4nth055/pythoncode-tutorials/tree/master/gui-programming/file-explorer

### 라이센스(참고 오픈소스)
MIT License<br/>
Copyright (c) 2019 Rockikz

### 세부 구현사항
Git Commands
git이 제공하는 커맨드를 <file>을 우클릭해서 원하는 커맨드를 선택하도록 구현함. 이때, 항상 모든 커맨드를 사용할 수 있는 것은 아니고 <file>의 status에 따라 사용 가능한 커맨드가 달라짐. status에 맞지 않는 커맨드를 입력받는 경우 에러 메세지만 출력하고 변화가 일어나지 않음<br/>
- git init <dir><br/>
1. init 되어 있지 않은 경로 <dir>에 깃 레포지토리를 만듦.<br/>
2. 하위 폴더 및 파일들도 레포지토리에 포함됨.<br/>
3. git init이 된 파일들은 이제 status를 확인할 수 있음.<br/>

- git status<br/>
1. 모든 상태에서 사용가능함.<br/>
2. 레포지토리에 속한 파일들의 status를 출력함<br/>

- git add <file><br/>
1. 모든 상태에서 사용가능함.<br/>
2. git add 후 <file>의 status는 staged.<br/>

- modified<br/>
1. 파일이 사용자에 의해 수정되는 경우 자동으로 modified로 status를 변경함.<br/>

- git restore <file><br/>
1. modified, staged 상태에서만 사용가능함.<br/>
2. git restore 후 파일은 수정되기 전으로 내용이 복귀됨.<br/>

- git rm <file><br/>
1. 모든 상태에서 사용가능함.<br/>
2. git rm 후 <file>의 status는 staged.<br/>
3. 로컬에서 <file> 이 제거됨.<br/>

- git rm --cached <file><br/>
1. 모든 상태에서 사용가능함.<br/>
2. git rm 후 <file>의 status는 staged.<br/>
3. 로컬에서 <file> 이 제거되지 않음.<br/>

- git mv <file><br/>
1. committed 상태에서만 사용가능함.<br/>
2. git mv 후 <file>의 status는 staged.<br/>
3. <file>의 이름이 변경됨.<br/>

- git commit -m <comment><br/>
1. staged 상태에서만 사용가능함.<br/>
2. commit 메세지를 입력받고 기록함.<br/>
3. commit 후 <file>의 status는 committed.<br/>
  
### 프로젝트 2<br/>
  
  Feature #1: Branch management 
   
  ![branch](https://github.com/ahnjh05141/oss_project_team2/assets/130345605/b9345a66-8f5c-4385-94e6-4aac804cb787)

   Branch 클릭 후, 사용자가 필요한 메뉴를 우클릭 후 작업을 수행할 수 있다. 
  
 
  Feature #2: Git Branch merge
  
  gitRepository.py 의 class Repository에 구현하였습니다. 사용자가 입력한 브랜치 이름으로부터, 브랜치 객체와 path를 파악하여 Master 브랜치와 병합할 수 있게 구현하였습니다. 기존 브랜치의 폴더를 Master 브랜치에 move 함으로써, 기존 커밋 내용이 사라지지 않는 것을 구현하였습니다.****
  Feature #3: Git commit history<br/>
  
  ![커밋히스토리 결과](https://github.com/ahnjh05141/oss_project_team2/assets/56011947/b6f28ef2-0cb8-4444-84cb-f6c766d7592a)
  
  우클릭 후, 커밋 히스토리를 클릭하면 나오는 화면, 각각의 점을 클릭하여 정보를 확인할 수 있다.<br/>
  
  Feature #4: Git clone Repository
  
  ![clone_image](https://github.com/ahnjh05141/oss_project_team2/assets/107451242/9564a805-1eab-431f-a013-ff9243197845)
  
  로컬 폴더를 우클릭 후, 클론 메뉴를 선택해 GitHub의 Repository를 복제할 수 있다.

