import os
import subprocess
import numpy as np
import copy


def Con_Christofides(position, sample_nodes, sample_file):
    sample_nodes = np.array(copy.deepcopy(sample_nodes))
    sample_data = position[sample_nodes]
    compute_data = []
    for i, x in enumerate(sample_data):
        compute_data.append([i, x[0]*10000, x[1]*10000])
    np.savetxt(sample_file, np.array(compute_data), fmt='%d')

    # 执行exe，christofides算法计算路径，返回最优路径序列
    ch_seq = execute_exe(sample_file, sample_nodes)
    # 计算路径序列长度
    ch_seq_pos = position[ch_seq]
    tilted_pos = np.concatenate((ch_seq_pos[1:], ch_seq_pos[-1:]), axis=0)
    ch_seq_length = np.sum(np.power(np.sum(np.power(tilted_pos - ch_seq_pos, 2), axis=1), 0.5), axis=0)  # 计算路径长度
    return ch_seq, ch_seq_length


def execute_exe(tsp_file, id_data):
    if not os.path.exists(tsp_file):  #  判断文件是否存在
        raise EnvironmentError("ERROR:failed found tsp file.")
    pos_data = np.loadtxt(tsp_file)   #  读取结点位置信息
    exe_path = r"compare_experiment/exe/christofides_tsp %s" % (tsp_file)
    rc, out = subprocess.getstatusoutput(exe_path)  # 执行christofides算法
    seq_id = []
    if rc == 0:  # 执行成功
        seq = out.split('\n')[-1].split(':')[-1].split(' ')[:-1]
        seq = [int(x) for x in seq]
        seq = seq[seq.index(0):] + seq[:seq.index(0)+1]  # 最优路径序列(索引)
        seq_id = id_data[np.array(seq)]    # 最优路径结点序列
        # 计算路径长度
        # pos_data = pos_data[seq]
        # tilted_pos = np.concatenate((pos_data[1:], pos_data[-1:]), axis=0)
        # length = np.sum(np.power(np.sum(np.power(tilted_pos - pos_data, 2), axis=1), 0.5), axis=0)  # 计算路径长度
        # print(seq_id)
        # print(length)
    return seq_id