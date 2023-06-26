###############################
## DBSCAN Clustering 알고리즘  ##
###############################

import sys
import math

sys.setrecursionlimit(10000) # recursion 제한 횟수 증가
input_file = sys.argv[1]  # input file name
n = int(sys.argv[2])         # number of clusters
Eps = int(sys.argv[3])      # Maximum radius of neighborhood
MinPts = int(sys.argv[4])    # Threshold

class DataPoint:
    id = 0
    x = 0.0
    y = 0.0
    label = False   # 특정 Cluster에 소속되었으면 True로 변경
    neighbors = []  # Data point의 이웃 data 저장

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

# 두 data point의 거리의 제곱을 계산
def dist(p, q):
    return math.pow(p.x - q.x, 2) + math.pow(p.y - q.y, 2)

# DB를 scan하면서 p의 neighbor를 찾음
def Neighbors(p):
    data = []
    for q in DB:
        if p == q:
            continue
        if dist(p, q) <= Eps*Eps:
            data.append(q)
    return data

# seed_set에 Density-Reachable한 모든 데이터들 clustering
def getCluster(p, seed_set):
    seed_set.append(p)
    for q in p.neighbors:
        if q.label == True:
            continue
        seed_set.append(q)
        q.label = True
        # q가 core point 일 경우 expansion
        if len(q.neighbors) >= MinPts:
            getCluster(q, seed_set)

DB = []
Cluster = []
fr = open(input_file, 'rt')

# input file을 읽고 DB에 저장
while True:
    line = fr.readline()
    if line == '':
        break
    id, x, y = line.split()
    id = int(id)
    x = float(x)
    y = float(y)
    DB.append(DataPoint(id, x, y))

# 각 데이터의 neighbor 정보 update
for p in DB:
    p.neighbors = Neighbors(p)

# clustering 알고리즘 진행
for p in DB:
    seed_set = []
    N = len(p.neighbors)
    # p가 이전에 Clustering 되었는지 && core point인지 확인
    if (p.label == True) | (N < MinPts):
        continue
    p.label = True
    getCluster(p, seed_set)
    Cluster.append(seed_set)

# 각각의 만들어진 Cluster을 크기순으로 정렬
sorted_cluster = sorted(Cluster, key=len, reverse=True)

# 상위의 n개의 cluster만 뽑아서 출력
for i in range(n):
    output_file = input_file[0:6] + '_cluster_' + str(i) + '.txt'
    fw = open(output_file, 'wt')
    for j in sorted_cluster[i]:
        line = str(j.id) + '\n'
        fw.write(line)

fr.close()
fw.close()



