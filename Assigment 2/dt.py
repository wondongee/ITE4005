import sys
import math

# Tree의 Node
class Node:
    def __init__(self):
        self.nextNode = []      # 자식 Node를 저장하는 배열
        self.feature = 'None'   # 노드가 분기하는 feature 저장
        self.label = 'None'     # leaf node일 경우 class label 저장
        self.leaf = 0           # leaf node일 경우 1로 변경
        self.category = 'None'  # 부모 노드 feature로부터 분기해 온 category 저장

# 현재 DB의 Entropy 계산
def Entropy(DB, feature_name, feature_category):
    n = len(feature_name)
    cls = tuple(feature_category[n-1])
    cnt = [0 for i in range(len(cls))]
    for t in DB:
        cnt[cls.index(t[n-1])] += 1
    entropy = 0
    for i in range(len(cnt)):
        if(cnt[i] == 0):
            continue
        ratio = cnt[i] / sum(cnt)
        entropy -= ratio * math.log2(ratio)
    return entropy

# DB를 idx번 feature로 분기할 때 얻는 GainRatio 계산
def GainRatio(DB, feature_name, feature_category, idx):

    # DB의 feature category 별로 subDB로 분리
    feature_trg = tuple(feature_category[idx])
    subDB = [ [] for i in range(len(feature_trg)) ]
    for t in DB:
        subDB[feature_trg.index(t[idx])].append(t)

    # 분기 후 Information Gain 계산
    ratio = []
    info_gain_af = 0
    for t in subDB:
        num = len(t)/len(DB)
        ratio.append(num)
        info_gain_af += Entropy(t, feature_name, feature_category) * num

    # 분기한 후 Split Info 계산
    info_split = 0
    for i in range(len(ratio)):
        if ratio[i] == 0:
            continue
        info_split -= ratio[i] * math.log2(ratio[i])

    # 최종 GainRatio 계산
    info_gain_bf = Entropy(DB, feature_name, feature_category)
    info_gain = info_gain_bf - info_gain_af
    gainRatio = info_gain / info_split
    return gainRatio

# training data로 Decision Tree를 구현
def BuildTree(DB, feature_name, feature_category, feature_chk, node):

    # 종료 조건 : 하나의 클래스 label만 남을 때
    if Entropy(DB, feature_name, feature_category) == 0:
        node.label = DB[0][-1]
        node.leaf = 1
        return node

    # 종료 조건 : 더 이상 나눌 feature가 없을 때 -> majority vote
    elif not (0 in feature_chk):
        n = len(feature_name)
        cls = tuple(feature_category[n - 1])
        cnt = [0 for i in range(len(cls))]
        for t in DB:
            cnt[cls.index(t[n - 1])] += 1
        major_index = cnt.idex(max(cnt))
        node.label = cls[major_index]
        node.leaf = 1
        return node

    # Gain Ratio가 최대가 되는 feature 선택
    max_infoGain = 0
    idx = 0
    for i in range(len(feature_name)-1):
        if(feature_chk[i] == 1):
            continue
        gain_ratio = GainRatio(DB, feature_name, feature_category, i)
        if max_infoGain < gain_ratio:
            idx = i
            max_infoGain = gain_ratio
    node.feature = feature_name[idx]

    # DB를 선택된 feature의 category 별로 split하여 subDB에 넣은 후 subDB 별로 자식노드 생성
    feature_chk[idx] = 1
    feature_trg = tuple(feature_category[idx])
    subDB = [ [] for i in range(len(feature_trg)) ]
    for t in DB:
        subDB[feature_trg.index(t[idx])].append(t)
    for t in subDB:
        newNode = Node()
        if len(t) != 0:
            newNode.category = t[0][idx]
            node.nextNode.append(newNode)
            new_feature_chk = feature_chk.copy()
            BuildTree(t, feature_name, feature_category, new_feature_chk, newNode)

# Decision Tree 통해 각 데이터의 결과 클래스 label 반환
def treeResult(node, tuple, feature_test_name):

    # leaf node이면 해당 노드의 class label 반환
    if node.leaf == 1:
        return node.label

    # leaf node를 찾을 때 까지 recursion
    for i in range(len(node.nextNode)):
        idx = feature_test_name.index(node.feature)
        if tuple[idx] == node.nextNode[i].category:
            result = treeResult(node.nextNode[i], tuple, feature_test_name)
            return result
    return 'invalid'

dt_train = sys.argv[1]
dt_test = sys.argv[2]
dt_result = sys.argv[3]
fr_train = open(dt_train, 'rt')
fr_test = open(dt_test, 'rt')
fw_result = open(dt_result, "wt")

DB = []
feature_name = fr_train.readline().split()  # 모든 feature name 저장
feature_category = []                       # 각 feature의 category set 저장
feature_chk = []                            # 모든 feature가 사용되었는지 여부 저장
for i in range(len(feature_name)):
    feature_category.append(set())
    feature_chk.append(0)

# dt_train 파일을 읽고 DB에 저장
while True:
    line = fr_train.readline()
    if line == '':
        break
    # 각 feature의 카테고리 저장
    i = 0
    line = line.split()
    for elem in line:
        feature_category[i].add(elem)
        i += 1
    # train data DB에 저장
    line = tuple(line)
    DB.append(line)

# root Node 생성
rootNode = Node()
# Decision Tree 생성
BuildTree(DB, feature_name, feature_category, feature_chk, rootNode)


# dt_test 파일을 읽고 결과값 dt_result에 저장
feature_test_name = fr_test.readline().split()
lines = str()
for t in tuple(feature_name):
    lines += t + '\t'
lines += '\n'
fw_result.write(lines)

while True:
    line = fr_test.readline()
    if line == '':
        break
    line = tuple(line.split())
    result = treeResult(rootNode, line, feature_test_name)
    lines = str()
    for t in line:
        lines += t + '\t'
    lines += result + '\n'
    fw_result.write(lines)


fr_train.close()
fr_test.close()
fw_result.close()