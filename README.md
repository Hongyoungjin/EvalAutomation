
# 창의적융합디자인 동료평가/발표평가 점수 합산

## Overview
창융디 평가 점수 계산 자동화 프로그랩입니다.

### Features
1. 창융디 발표평가 (팀별 평가)와 동료평가 점수를 합산합니다.
2. 출석부 순서대로 각 학생의 동료평가 점수와 팀 점수, 그리고 합산한 점수를 계산합니다.

### 주의사항

1. 해당 스크립트는 엑셀 파일 (.xlsx 형식)만 인식하고 점수에 반영합니다.
2. 학생들이 양식에 맞추지 않아 워드, pdf, jpeg 등의 형식으로 제출한 것은 바로 무시해버립니다. 
3. 사전에 학생들에게 관련 내용을 강조하여 안내해야 하고, 프로그램이 미처 인식하지 못한 파일들은 직접 확인해서 반영하셔야 합니다. 
4. pdf나 word 형식의 파일의 경우에는 [확장자 변환 사이트](https://convertio.co/kr/) 를 통해 변환할 수 있으니 이 또한 참고하시길 바랍니다. 

## How to run

### 패키지 설치
파이썬 코드에서 요구하는 패키지들을 미리 설치합시다.

''' 
git clone https://github.com/Hongyoungjin/EvalAutomation.
pip install .
 
'''

### 필요한 파일 만들기

[출석부 다운로드 받기]
1. 아이캠퍼스 > 출결/학습 현황 > 주차별 출결 합산 > 엑셀 다운로드
2. csv 형식의 파일로 설치되므로 [확장자 변환 사이트](https://convertio.co/kr/csv-xlsx/)를 통해 xlsx 형식으로 바꿔줍니다.
3. 다운로드 받은 엑셀 파일은 students 안에 넣어줍니다.

[팀별 학생 리스트 만들기]
1. 조별로 학생들을 배치한 내용을 기반으로 1조부터 맨 끝 조까지 일렬로 나열합니다.
2. 첫 번째 열은 몇 번째 조인지 (ex. 1,2,3,.....,17) 적습니다
3. 두 번째 열은 일렬로 나열한 학생들을 차례대로 나열해줍니다.
4. 해당 파일은 teams 안에 넣어줍니다. 

**- 깃허브 teams 파일 안에 예시 파일이 있으니 이를 참고하세요**

**- 중간발표 때 팀 배치와 기말발표 때 팀 배치를 헷갈리면 안됩니다**

[과제 다운로드 받기]
1. 아이캠퍼스 > 과제 및 평가 > 발표평가 제출 과제란 > 제출물 다운로드
2. 해당 파일들은 assignments 폴더 안에서 압축을 해제합니다.

**- 중간발표 때 팀 배치와 기말발표 때 팀 배치를 헷갈리면 안됩니다**


### 파이썬 스크립트 돌리기

1. 스크립트가 있는 디렉토리에서 evals.py 스크립트를 실행해줍니다. 
2. *session* 옵션: 중간 발표일 경우 **m**, 기말 발표일 경우 **f** 를 입력합니다.
3. *team* 옵션: 해당 분반에 최대 몇 명이 있는지 적습니다.
4. *member* 옵션: 각 팀의 최대 인원을 적습니다. 

따라서 ***기말 발표*** 결과를 합산하고 싶고,
분반에 ***총 17 팀***이 있으며,
각 팀에 ***최대 6명의 팀원***이 있는 경우 아래와 같이 입력해서 실행합니다. 

'''
python3 evals.py --session f --team 17 --member 6 

'''

## Troubleshooting

### 디버깅하는 방법
학생들이 제출 시 안내사항을 제대로 듣지 않고 제출하는 경우가 많으므로 처음에 실행할 때는 거의 항상 중간에 오류가 뜹니다. 

디버깅을 최대한 쉽게 하기 위해 중간 중간에 어떤 프로세스가 끝났는지, 어떤 학생의 과제물을 확인하다가 멈췄는지, 그리고 어떤 학생을 확안하는 중에 멈췄는지 log가 나오게끔 설정했습니다. 

따라서 오류가 생길 경우 놀라지 말고 마지막으로 창에 나온 엑셀파일로 들어가서 오타나 오류를 수정하고 다시 실행하면 원활히 실행할 수 있을 것입니다. 

아래는 학생들이 자주 범하는 오류들입니다. 

[1. 팀별 학생 리스트 만들 때]
1. 학생 이름 + 학번에서 이름과 학번 사이의 공백이 없어야 합니다. 

[2. 동료 평가]
1. 학생 이름이 잘못된 경우 (대부분 성을 잘못 쓴다)
2. 제출자가 자신의 이름까지 넣은 경우: 삭제해준다.
3. 이름 란에 이름 이외의 그 어떤 것도 있으면 안됨 (앞뒤에 공백이 있어서도 안됨)
4. 점수 란에 숫자 이외의 그 어떤 것도 있으면 안됨 (앞뒤에 공백이 있어서도 안됨)

[최종 평가]
1. 학생 이름 + 학번에서 이름과 학번 사이의 공백이 없어야 함. (1.1 위반)


