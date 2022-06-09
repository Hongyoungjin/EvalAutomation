from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import numpy as  np
import string
import glob
import random

def remove_vulnerabilities(dataframe, arg):
    # Remove NaN values
    dataframe = dataframe.fillna(0)
    # Remove elements that are not float
    for row in range(dataframe.shape[0]):
        if arg == "team":
            for col in range(dataframe.shape[1]):
                if dataframe.iloc[row,col] *0 != 0:
                    dataframe.iloc[row,col] = np.float(0)
                else: 
                    continue
        elif arg == "individual":
            for col in range(1, dataframe.shape[1]):
                if dataframe.iloc[row,col] *0 != 0:
                    dataframe.iloc[row,col] = np.float(0)
                else: 
                    continue

    return dataframe
   

path = './assignments/'
files = glob.glob(path + "*.xlsx")
files_peer = [s for s in files if "동료" in s]
files_team = [s for s in files if "발표" in s]

team_no = input("총 몇 조까지 있나요? (자연수로 입력) : ")
team_no = int(team_no)
team_index = string.ascii_letters[team_no]
team_index = team_index.upper()
team_range = "B : " + team_index

mate_no = input("한 팀에 최대 몇 명까지 있나요? (자연수로 입력) :  ")
mate_no = int(mate_no)
mate_index = string.ascii_letters[mate_no]
mate_index = mate_index.upper()
mate_range = "B : " + mate_index

array_team = np.zeros([6,team_no])

## 발표 평가지 평가
for file_name in files_team:
    print(file_name)
    df = pd.read_excel(file_name, usecols=team_range, nrows=10, skiprows=5)
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
result_df.to_excel('./evals/TeamScores.xlsx')

print("---------------------------------------------------------------------")
print("---------------------Team Evaluation Done----------------------------")
print("---------------------------------------------------------------------")

## 동료 평가지 평가
file_peer = glob.glob('./teams/' + "*.xlsx")
print(file_peer)
team_dist = pd.read_excel(file_peer[0], usecols='A:B', header = None, nrows=team_no * mate_no)
team_dist = pd.concat([team_dist, pd.DataFrame(np.zeros([team_dist.shape[0],8]))], axis=1)
team_dist = np.array(team_dist)

for file_name in files_peer:
    print(file_name)
    df = pd.read_excel(file_name, usecols=mate_range, nrows=6, skiprows=6, header=None)
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
peer_result.to_excel('./evals/IndividualScores.xlsx')

print("---------------------------------------------------------------------")
print("---------------------Peer Evaluation Done----------------------------")
print("---------------------------------------------------------------------")


## 출석부에 총 점수 계산 (출석부 순서대로)

attendance = glob.glob('./students/' + "*.xlsx")
indiv_score = peer_result[['이름_학번', '총점', '팀 점수', '최종 점수']]
indiv_score = np.array(indiv_score)


attendance = pd.read_excel(attendance[0], usecols='B')
FinalScore = pd.concat([attendance, pd.DataFrame(np.zeros([attendance.shape[0],3]))], axis=1)
FinalScore = np.array(FinalScore)
print("Before: ",FinalScore)

for std in range(indiv_score.shape[0]):
    where = int(np.where(FinalScore==indiv_score[std,0])[0])
    FinalScore[where] = indiv_score[std]

print("After: ",FinalScore)

final_result = pd.DataFrame(FinalScore)
final_result.columns = ['이름_학번', '동료 평가 점수', '팀 점수', '최종 점수']
final_result.to_excel('./evals/FinalScore.xlsx')

print("---------------------------------------------------------------------")
print("---------------------Total Score Written-----------------------------")
print("---------------------------------------------------------------------")