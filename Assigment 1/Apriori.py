from itertools import combinations

minSup, readFileName, writeFileName = input().split()
minSup = int(minSup)
maxIndexItem = 0 # Item 중 index 값이 제일 높은 것 ex) 0~19이면 19
DB = list()
fw = open(writeFileName, 'wt')
fr = open(readFileName, "rt")

# 파일 읽고 DB에 거래내역 저장
while True:
    line = fr.readline()
    if line == '':
        break
    line = set(map(int, line.split()))
    DB.append(line)
    if max(line) > maxIndexItem:
        maxIndexItem = max(line)
totalNum = len(DB)
totalList = list()

# DB scan -> Candidate_1 구함
cList = [0 for i in range(maxIndexItem + 1)]
for a in DB:
    for i in range(maxIndexItem + 1):
        if {i}.issubset(a):
            cList[i] += 1

# Candidate_1 -> Frequent List_1 구함
fList = list()
plunnedSet = list()
result = list()
for i in range(maxIndexItem + 1):
    cList[i] /= totalNum
    if cList[i] >= (minSup/100.0):
        result.append(cList[i]*totalNum)
        fList.append({i})
    else:
        plunnedSet.append({i})
totalList.append(fList)


# repeat with index[k] -> Frequent Pattern 모두 구하여 totalList에 저장
for k in range(2, maxIndexItem + 1):
    cList = list()
    
    # self-joining L_k -> C_k+1
    for i in range(len(fList)):
        for j in range(i + 1, len(fList)):
            if len(fList[i] | fList[j]) == k:
                cList.append(fList[i] | fList[j])

    # C_k+1에서 중복값 제거
    result = [] # 중복 제거된 값들이 들어갈 리스트
    for value in cList:
        if value not in result:
            result.append(value)
    cList = result

    # C_k+1에서 plunning
    result = []
    for a in cList:
        if len(plunnedSet) == 0:
            break
        for b in plunnedSet:
            if a.issuperset(b):
                cList.remove(a)
                break

    # DB scan -> C_k+1 frequent count
    cnt = [0 for i in range(len(cList))]
    for a in DB:
        for i in range(len(cList)):
            if cList[i].issubset(a):
                cnt[i] += 1

    # C_k+1 -> L_k+1 구함
    fList = list()
    plunnedSet = list()
    result = list()
    for i in range(len(cList)):
        cnt[i] /= totalNum
        if cnt[i] >= (minSup / 100):
            fList.append(cList[i])
            result.append(cnt[i]*totalNum)
        else:
            plunnedSet.append(cList[i])

    # Terminate 조건 (L_k+1의 원소 x)
    if len(fList) == 0:
        break
    # Frequent Pattern(L_k+1)을 totalList에 저장
    totalList.append(fList)

# Frequent Pattern(totalList)에서 Association rule 적용
for itemSet in totalList:
    for item in itemSet:
        if len(item) == 1:
            continue
        else:
            sup = 0
            for a in DB:
                if item.issubset(a):
                    sup += 1
            for i in range(1, len(item)):
                c = combinations(item, i)
                c = list(c)
                for item2 in c:
                    conf = 0
                    item2 = set(item2)
                    for a in DB:
                        if item2.issubset(a):
                            conf += 1
                    # support와 confidence 출력
                    lines = str(item2) + '\t' + str(item - item2) + '\t' + str(round(sup / totalNum * 100, 2))\
                            + '\t' + str(round(sup / conf * 100, 2)) + '\n'
                    fw.write(lines)

fr.close()
fw.close()