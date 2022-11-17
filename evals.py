
import pandas as pd
import numpy as  np
import string
import glob
import random
from functions import args , remove_vulnerabilities
   


term = args()["session"]
team_no = args()["team"]
mate_no = args()["member"]

path = './assignments/'
files = glob.glob(path + "*.xlsx")
files_peer = [s for s in files if "동료" in s]
files_team = [s for s in files if "발표" in s]

team_index = string.ascii_letters[team_no]
team_index = team_index.upper()
team_range = "B : " + team_index

mate_index = string.ascii_letters[mate_no]
mate_index = mate_index.upper()
mate_range = "B : " + mate_index

array_team = np.zeros([6,team_no])

print("---------------------------------------------------------------------")
print("---------------------Team Evaluation Start-----------------------------")
print("---------------------------------------------------------------------")

## 발표 평가지 평가
for file_name in files_team:
    print(file_name)
    df = pd.read_excel(file_name,  engine='openpyxl',usecols=team_range, nrows=10, skiprows=5)
    if term == 'm':
        df = df.iloc[::2] # 중간에 있는 공백을 제거하기 위해서
    elif term == 'f':
        df = df.iloc[1::2] # 중간에 있는 공백을 제거하기 위해서
    df = remove_vulnerabilities(df,"team")

    # (확실히 하기 위해) 각 팀별 총점 다시 계산
    df = df.to_numpy()
    scores = np.zeros([team_no])
    for s in range(5):
        scores = scores + df[s]
    df = np.append(df, scores.reshape(1,-1),axis=0)
    
    array_team = array_team + df

result_np = array_team/len(files_team)
result_df = pd.DataFrame(result_np)
result_df.index = ['디자인 목적 부합성', '디자인 과정의 논리성', '최종 아이디어(솔루션)의 독창성', '프로토타입의 구체성', '발표자료 구성 및 발표력', '총점']
cols = list(range(1,team_no + 1))
for i in range(team_no):
    cols[i] = str(i+1) + " 조"
result_df.columns = cols

print("---------------------------------------------------------------------")
print("---------------------Peer Evaluation Start---------------------------")
print("---------------------------------------------------------------------")

## 동료 평가지 평가
file_peer = glob.glob('./teams/' + "*.xlsx")
print(file_peer)
team_dist = pd.read_excel(file_peer[0], engine='openpyxl', usecols='A:B', header = None, nrows=team_no * mate_no)
team_dist = pd.concat([team_dist, pd.DataFrame(np.zeros([team_dist.shape[0],8]))], axis=1)
team_dist = np.array(team_dist)

for file_name in files_peer:
    print(file_name)
    df = pd.read_excel(file_name, engine='openpyxl', usecols=mate_range, nrows=6, skiprows=6, header=None)
    df = remove_vulnerabilities(df, "individual")
    df = df.to_numpy()
    mates = np.array([r for r in df[:,0] if type(r) == str])
    mate_no_tmp = len(mates)
# 각 사람마다 값 더하기
    row = 0
    team_num = 0 # 현재 학생이 속한 조 번호
    while row < mate_no_tmp:
        name = df[row, 0]
        print("지금 확인하고 있는 학생 이름:  ",name)
        score_now = df[row][1:5]

        # (확실히 하기 위해) 각 팀별 총점 다시 계산
        total_score = score_now.sum()
        score_now = np.append(score_now,total_score)
      
        if type(name) == int:
            break


        name_id = np.array([r for r in team_dist[:,1] if name in r])
        print(name_id)

        # 한 분반에 동명이인이 있는 경우
        if len(name_id) > 1:

            # 동명이인이 어느 조인지를 타 팀원으로부터 미리 유추한 상태여야 함.
            # 동명이인이 동료평가 첫 줄이면 다른 줄과 바꿔서 미리 조 이름을 유추해야 함. 
            if row == 0:
                row_random = random.randrange(1, mate_no_tmp)
                df[[0,row_random]] = df[[row_random,0]]

                row = -1
                continue

            # 해당 동명이인 찾기
            dup_team_list = []
            dup_in_same_team = 0
            for dup in range(len(name_id)):
                # 출석부 상에서의 해당 학생의 인덱스
                dup_index = int(np.where(team_dist == name_id[dup])[0])

                # 출석부 상에서의 해당 학생이 속한 조 이름

                team_where = team_dist[dup_index,0]
                dup_name_id = name_id[dup]

                # 해당 학생이 해당 조 안에 있는지 확인
                if team_where == team_num:

                    dup_in_same_team += 1

                    team_dist[dup_index][2:7]  += score_now
                    team_dist[dup_index][7]    += 1

                    if dup_in_same_team == 2:
                        print("Duplicate Alert: 같은 조에 동명이인이 있으므로 Assingments 파일에서 해당 파일들을 따로 처리해야 함.")
                        exit()

                    # 학생이 속한 조의 발표점수
                    team_score = result_np[5 , team_num -1]
                    team_dist[dup_index][8] += team_score

        else: 
            if name == "이성준":
                print(team_no)
                print(mate_no)
            where = int(np.where(team_dist == name_id[0])[0])
            team_num = team_dist[where][0]
            team_dist[where][2:7]  += score_now
            team_dist[where][7]    += 1

            # 학생이 속한 조의 발표점수
            team_score = result_np[5 , team_num -1]
            team_dist[where][8]    += team_score

        
        row += 1
    print("현재 조 이름: ", team_num)

# 평균내기

for row in range(team_dist.shape[0]):
    try:
        team_dist[row][2:7] /= team_dist[row][7] # 평균점수 내기
        team_dist[row][8  ] /= team_dist[row][7] # 찐 팀별 점수 내기
        team_dist[row][9  ] = team_dist[row][6] + team_dist[row][8] # 최종 점수 = 개인 총점 + 팀별 점수
        

    except ZeroDivisionError:
        continue
    

peer_result = pd.DataFrame(team_dist)
peer_result.columns = ['팀 이름', '이름_학번', '아이디어발상', '아이디어평가/선정 및 구체스케치', '프로토타입 제작' , '발표자료 제작 및 발표', '총점', '평가받은 횟수', '팀 점수', '최종 점수']

print("---------------------------------------------------------------------")
print("---------------------Final Evaluation Start----------------------------")
print("---------------------------------------------------------------------")


## 출석부에 총 점수 계산 (출석부 순서대로)

attendance = glob.glob('./students/' + "*.xlsx")
indiv_score = peer_result[['이름_학번', '총점', '팀 점수', '최종 점수']]
indiv_score = np.array(indiv_score)


attendance = pd.read_excel(attendance[0], engine='openpyxl', usecols='B')
FinalScore = pd.concat([attendance, pd.DataFrame(np.zeros([attendance.shape[0],3]))], axis=1)
FinalScore = np.array(FinalScore)

for std in range(indiv_score.shape[0]):
    print(indiv_score[std,0])
    where = int(np.where(FinalScore==indiv_score[std,0])[0])
    FinalScore[where] = indiv_score[std]

final_result = pd.DataFrame(FinalScore)
final_result.columns = ['이름_학번', '동료 평가 점수', '팀 점수', '최종 점수']

## 엑셀 파일로 저장하기
if term == 'm':
    result_df.to_excel('./evals/팀별평가_중간.xlsx')
    peer_result.to_excel('./evals/동료평가_중간.xlsx')
    final_result.to_excel('./evals/최종평가_중간.xlsx')
elif term == 'f':
    result_df.to_excel('./evals/팀별평가_기말.xlsx')
    peer_result.to_excel('./evals/동료평가_기말.xlsx')
    final_result.to_excel('./evals/최종평가_기말.xlsx')
else:
    print("중간/기말 잘못 입력 하셨습니다. 다시 입력하세요.")

print("---------------------------------------------------------------------")
print("---------------------Entire Process Finished-------------------------")
print("---------------------------------------------------------------------")
