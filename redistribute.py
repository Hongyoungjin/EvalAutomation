import pandas as pd
import numpy as  np
import glob
from functions import args


team_no = args()["team"]
mate_no = args()["member"]


original_team = glob.glob('./teams/' + "*.xlsx")
original_team = pd.read_excel(original_team[0], usecols='A:B', header=None)
original_team.columns = ["team_name", "student_name"]

if original_team.shape[0] > team_no * mate_no:
  print("수용하지 못하는 인원이 있습니다. 팀 수를 늘리거나 최대 팀원 수를 늘려야 합니다.")
  exit()

new_team = pd.DataFrame(np.zeros([mate_no,team_no]))
names = list(original_team["student_name"])
i = 0

for row in range(mate_no):
  for col in range(team_no):
    if i == len(names):
      break
    new_team.iloc[row,col] = names[i]
    i+=1

# 엑셀 꾸미기
cols = list(range(1,team_no + 1))
indices = list(range(1,mate_no + 1))

for i in range(team_no):
    cols[i] = str(i+1) + " 조"

for j in range(mate_no):
    indices[j] = "팀원 " + str(j+1)

new_team.columns = cols
new_team.index = indices
print(new_team)
new_team.to_excel('./new_team/NewTeam.xlsx')
print("---------------------------------------------------------------------")
print("--------------------- Redistribution Done ---------------------------")
print("---------------------------------------------------------------------")

for i in range(team_no):
    cols[i] = i + 1
new_team.columns = cols

new_team_long = pd.DataFrame()

for i in range(1, team_no + 1):

  each_team = new_team[i]
  each_team = each_team.to_numpy()

  mates = pd.DataFrame([r for r in each_team if type(r) == str])
  team_num = pd.DataFrame(np.full(len(mates), i))

  new_team_chunk = pd.concat([team_num, mates], axis=1)
  new_team_long = pd.concat([new_team_long, new_team_chunk], axis=0)
print(new_team[2])

print("---------------------------------------------------------------------")
print("------------ New team for Final Automation Created ------------------")
print("---------------------------------------------------------------------")