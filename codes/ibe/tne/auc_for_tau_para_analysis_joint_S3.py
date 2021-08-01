'''
https://www.bilibili.com/video/av67331139/?p=2 神经网络讲解超好
数据是管理的依据和基础，也是挖掘算法的基础，用事实说话，事实与结果有直接因果关系，事实是自由行为模式下的轨迹，也就是自由行为模式的采样
中西方对自由的理解不同，西方是制度下的自由，也就是制定制度是在制度的约束下，中国是自由下的制度，制定制定是想当然地制定制度，也就是说中国的自由度更大，可以突破制度
'''
import random
# import os
import numpy as np

#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from config import *
#######################
def auc(myvecfile, dataset):
    node2vec = {}
    f = open(myvecfile, 'rb')
    # print(mypath1)
    # f = open('temp/zhihu_pages_score_merge_stock13.txt', 'rb')    # open函数，发现参数写为‘wb’，即按二进制write
    # f = open('temp/embed.txt', 'rb')    # open函数，发现参数写为‘wb’，即按二进制write
    for i, j in enumerate(f):           # enumerate(sequence, [start=0]), sequence：一个序列、迭代器或其他支持迭代对象,提取节点号i,节点嵌入j
        if j.decode() != '\n':
            node2vec[i] = list(map(float, j.strip().decode().split()))

    # huganglin
    graphtestfile=basepath + '/' + dataset +'/graph_test.txt'
    # print(graphtestfile)
    # graphtestfile=mypath+'/edgelistMergeFile/graph_train.txt'
    with open(graphtestfile, 'rb') as f1:
        edges = [list(map(int, i.strip().decode().split())) for i in f1]
    nodes = list(set([i for j in edges for i in j]))
    # print("nodes:",nodes)
    a = 0
    b = 0
    t1=0
    t2=0
    # tn=0 # 循环次数
    for i, j in edges:
        # tn=tn+1
        if i in node2vec.keys() and j in node2vec.keys():
            dot1 = np.dot(node2vec[i], node2vec[j])             # x.dot(y) 等价于 np.dot(x,y) ———x是m*n 矩阵 ，y是n*m矩阵，则x.dot(y) 得到m*m 矩阵
            random_node = random.sample(nodes, 1)[0]            # random.sample(list,n)随机采样列表list 的指定长度n 的随机样本，但是不会改变列表本身的排序
            while random_node == j or random_node not in node2vec.keys():  # 当random_node == j 时重新采样random_node，直到不相等
                random_node = random.sample(nodes, 1)[0]
            dot2 = np.dot(node2vec[i], node2vec[random_node])
            if dot1 > dot2:         # dot1 是边的两个顶点向量点乘值， dot2 是固定x， 随机选取不等于y的的值与x 做点乘得到的值， 如果dot1 > dot2 则边的x，y顶点更相似
                a += 1
                t1=t1+1
            elif dot1 == dot2:      # 如果dot1 == dot2 则边的x，y顶点与x，other顶点一样相似
                a += 0.5
                t2=t2+1
            b += 1
            # if tn%1000==0:
            #     print("Auc value:",tn,":",float(a) / b)
    # random.sample
    print("Auc value:", float(a) / b)
    return(float(a) / b)

def list_alltopicfile(mydata):
    mypath = basepath + '/'+mydata+'/topic_matrix'
    # print(mypath)
    L=[]
    li_temp = []
    for root, dirs, files in os.walk(mypath):
        for file in files:
            mystr=os.path.splitext(file)[0]
            location=int(mystr.find('_'))
            L.append(int(mystr[0:location])) #其中os.path.splitext()函数将路径拆分为文件名+扩展名
        li_temp.append(mypath + '/' + str(max(L))+ '_topicMatrix.txt')
    return li_temp


def list_byjointfile(mydata, mymethod):
    mypath = basepath + '/' + mydata + '/tau_para_analysis_joint/' + mymethod
    # print(mypath)
    li_name = []
    li_temp = []
    for root, dirs, files in os.walk(mypath):
        print('\n')
        files = strSort(files)
        print('files of ', mydata, ': ', mymethod + '_train_sort_noid.txt')
        print(files)

        method_vector = basepath + '/' + mydata + '/method_vector/' + mymethod + '_train_sort_noid.txt'
        li_name.append(method_vector)
        for file in files:
            # mystr=os.path.splitext(file)[0]
            # li_temp = mystr.split('_')

            # print(mypath + '/' + mystr + '.txt')
            li_name.append(mypath + '/' + file) #其中os.path.splitext()函数将路径拆分为文件名+扩展名
        return(li_name)
# -------取列表中字符串元素子串排序 create by huganglin20210216---------------
import re
def sort_key(s): #取数字子串：'字符_数字_字符'
    if s:
        try:
            # print('s:',s)
            c = re.findall(r'_(-?\d+)_',s)
            # print('cc:', c)
        except:
            c = -1
        # print('c:',c[0])
        return(int(c[0]))
def strSort(alist):  #列表排序key=sort_key
    alist.sort(key=sort_key,reverse=False)
    return(alist)
# /----------------------

if __name__ == "__main__":
    for mydata in datasets:  # 遍历数据集 modify by huganglin 20200131
        for mymethod in methods:
            # ------只有zhihu和cana数据集有这两个方法文本属性数据------
            if mymethod == 'CANE':
                if mydata == 'wiki' or mydata == 'citeseer' or mydata == 'blogCatalog' or mydata == 'cora_feature2708':
                    print('CANE continue:', mydata, '--', mymethod)
                    print('\n')
                    continue
            if mymethod == 'TADW':
                if mydata != 'cora_feature2708':
                    print('TADW continue:', mydata, '--', mymethod)
                    print('\n')
                    continue
            # /----------------------------------------------------------
            file = list_byjointfile(mydata, mymethod)
            for f in file:
                # print(f)
                auc(f, mydata)
            print('\n')
        print('\n')
        print('\n')