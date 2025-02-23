
import os
import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt

ROOT = os.getcwd()
DATA = "/random bus generator/" + "data/"
RESULT = "/random bus generator/" + "result/"
BUS = "bus-1062"
BRANCH = "branch-1062"

CSV = ".csv"
JSON = ".json"

BUS_PATH = ROOT + DATA + BUS + CSV
BRANCH_PATH = ROOT + DATA + BRANCH + CSV

def make_random_bus_position(path):  
    # bus 데이터 읽기
    bus_data = pd.read_csv(path)
    print("get bus data", bus_data, "*"*10, end="\n")
    
    # bus 개수 가져오기
    row_count = len(bus_data.index)
    print("bus data row count", row_count, type(row_count), "\n", "*"*10) # row_count = 1062
    
    additional_width = 0.1

    # bus 들이 들어갈 그리드셀 너비
    square_width = round(row_count) # 여유롭게 만들기 위해 +20 임시 할당
    # print('sq value : ', square_width)
    # bus들 리스트 만들고 섞기
    bus_id = list(range(1,row_count+1))
    random.shuffle(bus_id)
    # print("shuffled bus id list:", bus_id, "\n", "*"*10)
    bus_coordinate = []
    
    randomX = []
    randomY = []
    for i in range(row_count): # 중복 제거 넣기
        # for j in range(square_width):
        a = random.randint(1, square_width)
        b = random.randint(1, square_width)
        
        while a in randomX:
            a = random.randint(1, square_width)
        randomX.append(a)
        # print('randomX :', randomX)
            
        while b in randomY:
            b = random.randint(1, square_width)
        randomY.append(b)
        # print('randomY : ', randomY)
            
           
    
    print('end\n')
    # 섞은 bus들에 좌표 붙이기
    count = 0
    for i in range(square_width): 
        for j in range(square_width):
            bus_coordinate.append({"bus id": bus_id[count], "x": randomX[count], "y": randomY[count]})
            count += 1
            
            if (count == row_count):
                break
            
        if (count == row_count):
            break
        
    # json 형태로 출력
    bus_coordinate = sorted(bus_coordinate, key = lambda x:(x['bus id']))
    bus_coordinate = pd.DataFrame(bus_coordinate)
    # print(bus_coordinate, "\n", "*"*10)
    bus_coordinate.to_json(ROOT + RESULT + BUS + " random position" + JSON)
    
def get_bus_degree(path):
    # branch 데이터 읽기
    branch_data = pd.read_csv(path)
    # print("get branch data", branch_data, "*"*10, end="\n")
    
    # branch 개수 가져오기
    row_count = len(branch_data.index)
    # print("branch data row count", row_count, type(row_count), "\n", "*"*10)
    
    # connected_bus: 각 bus간 연결된 bus들을 리스트로 저장
    connected_bus = []
    for i in range(1062):
        connected_bus.append([])
    # print("connected_bus list initialize...")
    # print(connected_bus, "\n", "*"*10)
        
    for i in range(row_count):
        try:
            start_bus = branch_data.iloc[i, 0] - 1
            end_bus = branch_data.iloc[i, 1] - 1
            
            connected_bus[start_bus].append(end_bus)
            connected_bus[end_bus].append(start_bus)
            
        except IndexError:
            print("IndexError!", start_bus, end_bus)
            
    # print("connected_bus list result")
    # print(connected_bus, "\n", "*"*10)
        
    # bus_degree: connected_bus를 통해 bus간 degree 값 가져오기
    bus_degree = []
    for i in range(1062):
        bus_degree.append({"bus id": i + 1, "degree": len(connected_bus[i])})
        
    # degree_checker: degree 값 당 bus 개수 저장
    degree_checker = []
    for i in range(max(map(only_degree, bus_degree)) + 1):
        degree_checker.append({"degree": i, "count": 0})
        
    for i in range(1062):
        degree_checker[bus_degree[i]["degree"]]["count"] += 1
    # print("bus degree data", degree_checker)    
        
    degree_checker = pd.DataFrame(degree_checker)
    # print("degree checker dataframe", degree_checker, "*"*10, sep="\n")

    # degree_checker를 bar chart 형태로 표현
    hist = degree_checker["count"].plot(kind="bar")
    hist.set_xticks(np.arange(13))
    plt.show()
    
    degree_checker.to_json(ROOT + RESULT + BUS + " degree" + JSON)
    
def only_degree(dic):
    return dic["degree"]

if __name__ == '__main__':
    # print(BUS_PATH)
    make_random_bus_position(BUS_PATH)
    # print(BRANCH_PATH)
    # get_bus_degree(BRANCH_PATH)          