import numpy as np
import copy
import random
import datetime


def pathCost(pathIndex, position):  # 计算路径序列cost
    p_cost = 0
    seq_pos = position[pathIndex]
    tilted_pos = np.concatenate((seq_pos[1:], seq_pos[-1:]), axis=0)
    p_cost = np.sum(np.power(np.sum(np.power(tilted_pos-seq_pos, 2), axis=1), 0.5), axis=0)  # 计算路径长度
    return p_cost


def reversePath(path):  # reverse path
    rePath = path.copy()
    rePath = rePath[::-1]
    return rePath


def generateRandomPath(best_path):  # random generate a new path
    best_path_c = copy.deepcopy(best_path)
    a = np.random.randint(1, len(best_path_c)-1)
    while True:
        b = np.random.randint(1, len(best_path_c)-1)
        if np.abs(a - b) >= 1:
            break
    if a > b:
        re_path = reversePath(best_path_c[b:a + 1])
        best_path_c[b:a + 1] = re_path
    else:
        re_path = reversePath(best_path_c[a:b + 1])
        best_path_c[a:b + 1] = re_path
    return best_path_c


 # position_data(np): 待访问节点位置信息, nodes(np/list):选择节点
def optTsp(position_data, nodes, max_count):  # random update path and search best path
    starttime = datetime.datetime.now()  # compute start time

    initPathIndex = list(range(len(position_data))) + [0]
    if len(initPathIndex) <= 3:
        path = nodes[initPathIndex]
        cost = pathCost(initPathIndex, position_data)
        endtime = datetime.datetime.now()  # compute end time
        runtime = (endtime - starttime).total_seconds()  # running time
        return path, cost, runtime

    initPathIndexCopy = copy.deepcopy(initPathIndex)
    temp = initPathIndexCopy[1:-1]
    random.shuffle(temp)
    initPathIndexCopy[1:-1] = temp
    bestPathIndex = initPathIndexCopy
    bestCost = pathCost(bestPathIndex, position_data)  # 初始路径序列花费
    count = 0
    while count < max_count:  # 最大迭代次数
        newPathIndex = generateRandomPath(bestPathIndex)  # 生成新的路径
        newCost = pathCost(newPathIndex, position_data)  # 计算新的花费
        if newCost < bestCost:  # 更新最优解
            bestPathIndex = newPathIndex
            bestCost = newCost
            count = 0
        else:
            count += 1
    path = np.array(nodes)[bestPathIndex]

    bestCost = round(bestCost, 4)
    
    endtime = datetime.datetime.now()  # compute end time
    runtime = (endtime - starttime).total_seconds()  # running time

    return path, bestCost, runtime


if __name__ == '__main__':
   pass