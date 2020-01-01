# *===================================*
# -*- coding: utf-8 -*-
# * Time : 2019-12-31 11:29
# * Author : zhangsf
# *===================================*
# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import pickle

file_rank = open('../data/test/成绩.txt', 'r')
file_library = open('../data/test/图书馆门禁.txt', 'r')
file_borrow = open('../data/test/借书.txt', 'r')
file_consume = open('../data/test/消费.txt', 'r')
file_type = open('../data/图书类别.txt', 'r')

'''
 学期 学号 图书馆门禁次数 食堂总消费 交通总消费 宿舍总消费 超市总消费 书类别  排名
'''
data = []
'''
读入成绩
'''
print("读入成绩---------开始")
line = file_rank.readline()
line = file_rank.readline()  # 直接读取第二行数据
while line:
    temp = []
    pre = 0
    # 对于每行line的每个字符 将其转化为数字形式并存储于数组中 最后\n两个字符不读
    while pre < len(line) - 3:
        if line[pre] != '\t':
            end = pre + 1
            while end < len(line) - 1:
                if line[end] == '\t':
                    # print(line[pre:end])
                    temp = temp + [int(line[pre:end])]
                    pre = end + 1
                    break
                else:
                    end = end + 1
        else:
            pre = pre + 1
            end = pre + 1
        # print("pre",pre)
        # print("len(line) - 2",len(line) - 2)

    # print("sss")
    data = data + [temp]
    # 接着读取下一行
    line = file_rank.readline()

print("读入成绩---------完成")
'''
以学号为主key 学期为负key进行排序
'''
data = sorted(data, key=lambda x: (x[1], x[0]))
print(data)
'''
读入图书馆门禁次数(学期计)
'''
print("读入图书馆门禁次数(学期计)----开始")
line = file_library.readline()
line = file_library.readline()  # 直接读取第二行数据
i = 0
# 初始化将所有的进入图书馆的门禁次数初始化置为0
while i < len(data):
    data[i] = data[i] + [0]
    i = i + 1
print(data)
data=np.zeros(shape=(len(data),6,31)).tolist();
# 开始读取图书馆门禁信息
while line:
    readtime = 0  # 记录读取次数 第一次读学期 第二次为学号
    xueqi = int(line[0:1])
    xuehao = 2
    end = 2
    while end < len(line) - 2:
        if line[end] == '\t':
            xuehao = int(line[2:end])
            break
        end += 1
    print("学号",xuehao,"学期",xueqi)
    index = (xuehao - 1) * 3 + xueqi - 1
    print("index", index)
    print(len(data))
    print(data[index])
    data[index][2] += 1
    line = file_library.readline()
    print(line)

print("----读入图书馆门禁次数(学期计)------完成")
'''
借书
'''
"""
读取书籍信息
"""
print("读取书籍信息------------开始")
BookInfo = dict()
BookClass = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'TB',
             'TD', 'TE', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TP', 'TQ', 'TS', 'TT', 'TU', 'TV', 'U', 'V',
             'X', 'Y', 'Z', 'OO']
'''
pickle.dump(BookInfo,open('BookInfo.pkl','wb'))
'''
'''
with open('../data/图书类别.txt', encoding = 'utf-8') as f:
    f.readline();
    for line in f:
        line = line.replace('\n', '')
        (BookNumber, bookclass) = line.split('\t');
        if not BookNumber.isdigit():
            continue

        BookInfo[BookNumber] = bookclass
'''
BookInfo = pickle.load(open('BookInfo.pkl', 'rb'))
zero43 = np.zeros(43, int).tolist()
i = 0
offset = 4
while i < len(data):
    data[i] += zero43
    i = i + 1
line = file_borrow.readline()
line = file_borrow.readline()

while line:
    (seme, sid, name, date, ent) = line.split('\t')
    index = (int(sid) - 1) * 3 + int(seme) - 1
    if name not in BookInfo.keys():
        data[index][43 + offset - 1] += 1
    else:
        i = 0
        while i < len(BookClass) - 1:
            if BookClass[i] == BookInfo[name]:
                break;
            i = i + 1
        data[index][i + +offset - 1] += 1
    line = file_borrow.readline()
print("读取书籍信息------------完成")
''' 学期、学号、排名、门禁、书籍信息 '''
pickle.dump(data, open('data_pre.pkl', 'wb'))
