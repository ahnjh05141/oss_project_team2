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
