# *===================================*
# -*- coding: utf-8 -*-
# coding: utf-8
# * Time : 2020-01-01 10:37
# * Author : zhangsf
# *===================================*
"""
读取消费信息[term, stuID, place, date, time, cost]
data、time两项暂定去除，不参与训练
bug: 排序前将学号及学期改为数字，否则排序会错误
"""

''' ------------------读取消费信息----------------------- '''
data = []
with open('../data/test/消费.txt', 'r', encoding='utf8') as f:
    f.readline()
    for line in f:
        line = line.replace('\n', '')
        tmp_list = line.split('\t')
        tmp_list = [int(tmp_list[0]), int(tmp_list[1]), tmp_list[2],
                    int(tmp_list[3]), int(tmp_list[4]), float(tmp_list[5])]
        data.append(tmp_list)

''' -------------------获得地点列表---------------------- '''
# 检查数据中的所有地点项
AllPlace = [i[2] for i in data]
AllPlace = list(set(AllPlace))
AllPlace.sort()
# 检查结果：['食堂', '交通', '超市', '宿舍', '教室', '图书馆', '打印']

''' --------------------进行排序--------------------- '''
# 排序顺序：学号 > 学期 > 地点
sort_list = sorted(data, key=lambda x: (x[1], x[0], x[2]))

''' ------------把相同地点的花费合并在一起------------- '''
# 把相同地点的花费合并到一起
resolve_list = []
iterator = 0
while iterator < len(sort_list):
    item = sort_list[iterator]

    # 获得基本信息
    info = item[:3]

    # 计算在某个地点的花费情况
    cost = item[-1]
    while iterator + 1 < len(sort_list) and info == sort_list[iterator + 1][:3]:
        iterator += 1
        cost += sort_list[iterator][-1]

    # 学号和学期转换为int类型，加入在某个地点处的消费情况
    info.append(round(cost, 2))
    resolve_list.append(info)

    iterator += 1
# 格式：[学期（int），学号（int），地点，花费（float）]

''' ----------把每学期每个同学的消费情况合并------------- '''
# 把每个学期每个同学的消费情况整理到一个数组中
header = AllPlace
iterator = 0
result = []
while iterator < len(resolve_list):
    item = resolve_list[iterator]

    # 获得基本信息
    info = item[:2]

    # 统计在每个地点的消费情况
    cost = dict()
    cost[item[2]] = item[3]
    while iterator + 1 < len(resolve_list) and info == resolve_list[iterator + 1][:2]:
        iterator += 1
        cost[resolve_list[iterator][2]] = resolve_list[iterator][3]

    # 整理到一个列表中
    cost_result = []
    for i in header:
        if i in cost.keys():
            cost_result.append(cost[i])
        else:
            cost_result.append(0)

    # 整合到一起
    info = info + cost_result
    result.append(info)

    iterator += 1

''' ------------------补全信息----------------------- '''
# 把缺失的信息填补（置为0） 538个人 * 3个学期
index = 0
CostInfo = []
for i in range(1, 538 + 1):
    for j in range(1, 3 + 1):
        if result[index][:2] == [j, i]:
            CostInfo.append(result[index])
            index += 1
        else:
            CostInfo.append([j, i, .0, .0, .0, .0, .0, .0, .0])

''' ------------------保存信息----------------------- '''
import pickle

# 保存
pickle.dump(AllPlace, open('AllPlace.pkl', 'wb'))
pickle.dump(CostInfo, open('CostInfo.pkl', 'wb'))

# 读取
# =============================================================================
# AllPlace = pickle.load(open('AllPlace.pkl', 'rb'))
# result = pickle.load(open('CostInfo.pkl', 'rb'))
# =============================================================================
