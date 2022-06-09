import argparse
import numpy as np

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


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--session", type=str, default="m", help="중간 평가면 m, 발표 평가면 f")
    ap.add_argument("-t", "--team", type=int, default=17, help="분반에 총 몇 조까지 있는지 자연수로 입력")
    ap.add_argument("-m", "--member", type=int, default=6, help="한 팀에 최대 몇 명까지 있는지 자연수로 입력")
    arguments =vars(ap.parse_args())
    return arguments